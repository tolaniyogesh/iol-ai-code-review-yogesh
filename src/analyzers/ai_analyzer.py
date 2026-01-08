import json
import re
from typing import List, Dict, Any
from src.models import ReviewComment, Severity, FileChange
from src.llm.base import BaseLLMProvider
from src.logger import setup_logger

logger = setup_logger(__name__)


class AIAnalyzer:
    def __init__(self, llm_provider: BaseLLMProvider):
        self.llm_provider = llm_provider
    
    async def analyze_changes(self, file_changes: List[FileChange], 
                             focus_areas: Dict[str, bool],
                             pr_context: str = "") -> List[ReviewComment]:
        all_comments = []
        
        for file_change in file_changes:
            if not file_change.patch:
                continue
            
            comments = await self._analyze_file_change(
                file_change, focus_areas, pr_context
            )
            all_comments.extend(comments)
        
        return all_comments
    
    async def _analyze_file_change(self, file_change: FileChange,
                                   focus_areas: Dict[str, bool],
                                   pr_context: str) -> List[ReviewComment]:
        prompt = self._build_review_prompt(file_change, focus_areas, pr_context)
        
        try:
            response = await self.llm_provider.generate_review(prompt, {
                "file_path": file_change.filename,
                "changes": file_change.patch
            })
            
            comments = self._parse_llm_response(response, file_change.filename)
            logger.info(f"AI analysis completed for {file_change.filename}: {len(comments)} comments")
            return comments
            
        except Exception as e:
            logger.error(f"AI analysis failed for {file_change.filename}: {str(e)}")
            return []
    
    def _build_review_prompt(self, file_change: FileChange,
                            focus_areas: Dict[str, bool],
                            pr_context: str) -> str:
        focus_list = [area.replace('_', ' ').title() 
                     for area, enabled in focus_areas.items() if enabled]
        
        prompt = f"""You are an expert code reviewer. Analyze the following code changes and provide detailed, actionable feedback.

**File:** {file_change.filename}
**Status:** {file_change.status}
**Changes:** +{file_change.additions} -{file_change.deletions}

**PR Context:**
{pr_context[:500] if pr_context else "No additional context provided"}

**Focus Areas:** {', '.join(focus_list)}

**Code Diff:**
```diff
{file_change.patch}
```

**Instructions:**
1. Analyze the code changes focusing on: {', '.join(focus_list)}
2. Identify issues with appropriate severity levels
3. Provide specific, actionable suggestions
4. Reference exact line numbers from the diff
5. Avoid obvious or trivial comments
6. Suggest concrete code improvements where applicable

**Output Format:**
Provide your review as a JSON array of comments. Each comment must have:
- line_number: The line number in the file (extract from diff @@ markers)
- severity: One of "critical", "warning", or "suggestion"
- category: One of "Security", "Performance", "Code Quality", "Best Practices", "Documentation"
- message: Clear, specific description of the issue
- suggestion: Concrete fix or improvement (optional)

Example:
```json
[
  {{
    "line_number": 45,
    "severity": "critical",
    "category": "Security",
    "message": "SQL injection vulnerability: User input is directly concatenated into SQL query",
    "suggestion": "Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))"
  }},
  {{
    "line_number": 52,
    "severity": "warning",
    "category": "Performance",
    "message": "N+1 query pattern detected in loop",
    "suggestion": "Use bulk query or join to fetch all related data at once"
  }}
]
```

Provide ONLY the JSON array, no additional text."""

        return prompt
    
    def _parse_llm_response(self, response: str, file_path: str) -> List[ReviewComment]:
        comments = []
        
        try:
            json_match = re.search(r'\[[\s\S]*\]', response)
            if json_match:
                json_str = json_match.group(0)
                parsed_comments = json.loads(json_str)
                
                for comment_data in parsed_comments:
                    try:
                        severity_map = {
                            'critical': Severity.CRITICAL,
                            'warning': Severity.WARNING,
                            'suggestion': Severity.SUGGESTION
                        }
                        
                        comment = ReviewComment(
                            file_path=file_path,
                            line_number=comment_data.get('line_number', 1),
                            severity=severity_map.get(
                                comment_data.get('severity', 'suggestion').lower(),
                                Severity.SUGGESTION
                            ),
                            category=comment_data.get('category', 'General'),
                            message=comment_data.get('message', ''),
                            suggestion=comment_data.get('suggestion')
                        )
                        comments.append(comment)
                    except Exception as e:
                        logger.warning(f"Failed to parse individual comment: {str(e)}")
                        continue
            else:
                logger.warning(f"No JSON array found in LLM response for {file_path}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error parsing LLM response: {str(e)}")
        
        return comments
