import fnmatch
from typing import List, Dict, Any
from src.models import ReviewComment, PRContext, Severity
from src.config import ReviewConfig
from src.github_client import GitHubClient
from src.analyzers.static_analyzer import StaticAnalyzer
from src.analyzers.ai_analyzer import AIAnalyzer
from src.llm.base import BaseLLMProvider
from src.logger import setup_logger

logger = setup_logger(__name__)


class CodeReviewer:
    def __init__(self, github_client: GitHubClient, 
                 llm_provider: BaseLLMProvider,
                 config: ReviewConfig):
        self.github_client = github_client
        self.static_analyzer = StaticAnalyzer()
        self.ai_analyzer = AIAnalyzer(llm_provider)
        self.config = config
    
    async def review_pull_request(self, pr_number: int) -> Dict[str, Any]:
        if not self.config.enabled:
            logger.info("Review is disabled in configuration")
            return {"status": "skipped", "reason": "disabled"}
        
        logger.info(f"Starting review for PR #{pr_number}")
        
        pr_context = self.github_client.get_pull_request(pr_number)
        
        filtered_files = self._filter_files(pr_context.files_changed)
        logger.info(f"Reviewing {len(filtered_files)} files (filtered from {len(pr_context.files_changed)})")
        
        all_comments = []
        
        for file_change in filtered_files:
            logger.info(f"Analyzing {file_change.filename}")
            
            content = self.github_client.get_file_content(
                file_change.filename, 
                pr_context.head_branch
            )
            
            if content and self.config.focus_areas.code_quality:
                static_comments = self.static_analyzer.analyze_file(
                    file_change.filename,
                    content,
                    [rule.dict() for rule in self.config.custom_rules]
                )
                all_comments.extend(static_comments)
        
        if any([self.config.focus_areas.security, 
                self.config.focus_areas.performance,
                self.config.focus_areas.best_practices]):
            pr_context_str = f"Title: {pr_context.title}\nDescription: {pr_context.description}"
            ai_comments = await self.ai_analyzer.analyze_changes(
                filtered_files,
                self.config.focus_areas.dict(),
                pr_context_str
            )
            all_comments.extend(ai_comments)
        
        all_comments = self._deduplicate_comments(all_comments)
        all_comments = self._filter_by_severity(all_comments)
        all_comments = self._limit_comments(all_comments)
        
        logger.info(f"Generated {len(all_comments)} review comments")
        
        await self._post_comments(pr_number, all_comments)
        
        summary = self._generate_summary(all_comments, pr_context)
        self.github_client.post_review_summary(pr_number, summary)
        
        should_block = self._should_block_pr(all_comments)
        
        return {
            "status": "completed",
            "pr_number": pr_number,
            "comments_posted": len(all_comments),
            "should_block": should_block,
            "summary": summary
        }
    
    def _filter_files(self, files):
        filtered = []
        for file in files:
            should_ignore = False
            for pattern in self.config.ignore_patterns:
                if fnmatch.fnmatch(file.filename, pattern):
                    should_ignore = True
                    break
            
            if not should_ignore:
                filtered.append(file)
        
        return filtered
    
    def _deduplicate_comments(self, comments: List[ReviewComment]) -> List[ReviewComment]:
        seen = set()
        unique_comments = []
        
        for comment in comments:
            key = (comment.file_path, comment.line_number, comment.message)
            if key not in seen:
                seen.add(key)
                unique_comments.append(comment)
        
        return unique_comments
    
    def _filter_by_severity(self, comments: List[ReviewComment]) -> List[ReviewComment]:
        min_severity = self.config.severity_config.min_severity_to_comment.lower()
        severity_order = {'critical': 3, 'warning': 2, 'suggestion': 1}
        min_level = severity_order.get(min_severity, 1)
        
        filtered = []
        for comment in comments:
            comment_level = severity_order.get(
                comment.severity.value.split()[1].lower(), 1
            )
            if comment_level >= min_level:
                filtered.append(comment)
        
        return filtered
    
    def _limit_comments(self, comments: List[ReviewComment]) -> List[ReviewComment]:
        comments_by_file = {}
        for comment in comments:
            if comment.file_path not in comments_by_file:
                comments_by_file[comment.file_path] = []
            comments_by_file[comment.file_path].append(comment)
        
        limited_comments = []
        for file_path, file_comments in comments_by_file.items():
            sorted_comments = sorted(
                file_comments,
                key=lambda c: (
                    3 if 'Critical' in c.severity.value else
                    2 if 'Warning' in c.severity.value else 1,
                    c.line_number
                ),
                reverse=True
            )
            limited_comments.extend(
                sorted_comments[:self.config.review_settings.max_comments_per_file]
            )
        
        limited_comments = sorted(
            limited_comments,
            key=lambda c: (
                3 if 'Critical' in c.severity.value else
                2 if 'Warning' in c.severity.value else 1
            ),
            reverse=True
        )[:self.config.review_settings.max_total_comments]
        
        return limited_comments
    
    async def _post_comments(self, pr_number: int, comments: List[ReviewComment]):
        commit_id = self.github_client.get_latest_commit(pr_number)
        
        for comment in comments:
            comment_body = self._format_comment(comment)
            self.github_client.post_review_comment(
                pr_number,
                commit_id,
                comment.file_path,
                comment.line_number,
                comment_body
            )
    
    def _format_comment(self, comment: ReviewComment) -> str:
        formatted = f"{comment.severity.value} **{comment.category}**\n\n"
        formatted += f"{comment.message}\n"
        
        if comment.suggestion:
            formatted += f"\n**Suggested Fix:**\n{comment.suggestion}\n"
        
        if comment.code_snippet:
            formatted += f"\n**Code:**\n```\n{comment.code_snippet}\n```\n"
        
        return formatted
    
    def _generate_summary(self, comments: List[ReviewComment], 
                         pr_context: PRContext) -> str:
        critical_count = sum(1 for c in comments if 'Critical' in c.severity.value)
        warning_count = sum(1 for c in comments if 'Warning' in c.severity.value)
        suggestion_count = sum(1 for c in comments if 'Suggestion' in c.severity.value)
        
        summary = f"## 🤖 AI Code Review Summary\n\n"
        summary += f"**PR:** #{pr_context.pr_number} - {pr_context.title}\n"
        summary += f"**Author:** @{pr_context.author}\n"
        summary += f"**Files Changed:** {len(pr_context.files_changed)}\n\n"
        
        summary += f"### 📊 Review Statistics\n\n"
        summary += f"- 🔴 Critical Issues: {critical_count}\n"
        summary += f"- 🟡 Warnings: {warning_count}\n"
        summary += f"- 🔵 Suggestions: {suggestion_count}\n"
        summary += f"- **Total Comments:** {len(comments)}\n\n"
        
        if critical_count > 0:
            summary += "### ⚠️ Critical Issues Found\n\n"
            summary += "This PR contains critical issues that should be addressed before merging.\n\n"
        elif warning_count > 0:
            summary += "### ⚠️ Warnings Found\n\n"
            summary += "This PR contains some warnings that should be reviewed.\n\n"
        else:
            summary += "### ✅ No Critical Issues\n\n"
            summary += "No critical issues or warnings found. Great work!\n\n"
        
        summary += "---\n"
        summary += "*This review was generated automatically by AI Code Review Assistant*\n"
        
        return summary
    
    def _should_block_pr(self, comments: List[ReviewComment]) -> bool:
        if self.config.severity_config.block_pr_on_critical:
            if any('Critical' in c.severity.value for c in comments):
                return True
        
        if self.config.severity_config.block_pr_on_warning:
            if any('Warning' in c.severity.value for c in comments):
                return True
        
        return False
