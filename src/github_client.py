from typing import List, Optional
from github import Github, GithubException
from src.models import FileChange, PRContext
from src.logger import setup_logger

logger = setup_logger(__name__)


class GitHubClient:
    def __init__(self, token: str, repository: str):
        self.client = Github(token)
        self.repo = self.client.get_repo(repository)
        self.repository = repository
    
    def get_pull_request(self, pr_number: int) -> PRContext:
        try:
            pr = self.repo.get_pull(pr_number)
            
            files_changed = []
            for file in pr.get_files():
                file_change = FileChange(
                    filename=file.filename,
                    status=file.status,
                    additions=file.additions,
                    deletions=file.deletions,
                    changes=file.changes,
                    patch=file.patch if hasattr(file, 'patch') else None
                )
                files_changed.append(file_change)
            
            pr_context = PRContext(
                pr_number=pr_number,
                title=pr.title,
                description=pr.body or "",
                author=pr.user.login,
                base_branch=pr.base.ref,
                head_branch=pr.head.ref,
                files_changed=files_changed
            )
            
            logger.info(f"Fetched PR #{pr_number}: {pr.title}")
            return pr_context
            
        except GithubException as e:
            logger.error(f"Failed to fetch PR #{pr_number}: {str(e)}")
            raise
    
    def get_file_content(self, file_path: str, ref: str) -> Optional[str]:
        try:
            content = self.repo.get_contents(file_path, ref=ref)
            if isinstance(content, list):
                return None
            return content.decoded_content.decode('utf-8')
        except GithubException as e:
            logger.warning(f"Could not fetch content for {file_path}: {str(e)}")
            return None
    
    def post_review_comment(self, pr_number: int, commit_id: str, 
                           file_path: str, line_number: int, comment: str):
        try:
            pr = self.repo.get_pull(pr_number)
            pr.create_review_comment(
                body=comment,
                commit=self.repo.get_commit(commit_id),
                path=file_path,
                line=line_number
            )
            logger.info(f"Posted comment on {file_path}:{line_number}")
        except GithubException as e:
            logger.error(f"Failed to post comment: {str(e)}")
            try:
                pr.create_issue_comment(
                    f"**Review Comment for `{file_path}:{line_number}`**\n\n{comment}"
                )
                logger.info(f"Posted as issue comment instead")
            except Exception as fallback_error:
                logger.error(f"Fallback comment also failed: {str(fallback_error)}")
    
    def post_review_summary(self, pr_number: int, summary: str, 
                           event: str = "COMMENT"):
        try:
            pr = self.repo.get_pull(pr_number)
            pr.create_review(body=summary, event=event)
            logger.info(f"Posted review summary for PR #{pr_number}")
        except GithubException as e:
            logger.error(f"Failed to post review summary: {str(e)}")
            raise
    
    def get_latest_commit(self, pr_number: int) -> str:
        try:
            pr = self.repo.get_pull(pr_number)
            commits = list(pr.get_commits())
            return commits[-1].sha if commits else ""
        except GithubException as e:
            logger.error(f"Failed to get latest commit: {str(e)}")
            raise
