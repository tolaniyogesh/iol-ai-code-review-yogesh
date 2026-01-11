from enum import Enum
from typing import Optional, List
from pydantic import BaseModel


class Severity(str, Enum):
    CRITICAL = "🔴 Critical"
    WARNING = "🟡 Warning"
    SUGGESTION = "🔵 Suggestion"


class ReviewComment(BaseModel):
    file_path: str
    line_number: int
    severity: Severity
    category: str
    message: str
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None


class FileChange(BaseModel):
    filename: str
    status: str
    additions: int
    deletions: int
    changes: int
    patch: Optional[str] = None
    content: Optional[str] = None


class PRContext(BaseModel):
    pr_number: int
    title: str
    description: str
    author: str
    base_branch: str
    head_branch: str
    files_changed: List[FileChange]
