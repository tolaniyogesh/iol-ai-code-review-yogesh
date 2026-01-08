import os
import yaml
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class CustomRule(BaseModel):
    name: str
    pattern: str
    severity: str
    message: str


class LanguageSpecific(BaseModel):
    max_function_length: Optional[int] = None
    max_complexity: Optional[int] = None
    require_docstrings: Optional[bool] = None
    max_method_length: Optional[int] = None
    require_javadoc: Optional[bool] = None
    prefer_const: Optional[bool] = None
    no_var: Optional[bool] = None


class FocusAreas(BaseModel):
    code_quality: bool = True
    security: bool = True
    performance: bool = True
    best_practices: bool = True
    documentation: bool = True


class SeverityConfig(BaseModel):
    block_pr_on_critical: bool = False
    block_pr_on_warning: bool = False
    min_severity_to_comment: str = "suggestion"


class ReviewSettings(BaseModel):
    max_comments_per_file: int = 10
    max_total_comments: int = 50
    avoid_obvious_comments: bool = True
    suggest_fixes: bool = True
    include_line_numbers: bool = True


class ReviewConfig(BaseModel):
    version: str = "1.0"
    enabled: bool = True
    ignore_patterns: List[str] = Field(default_factory=list)
    focus_areas: FocusAreas = Field(default_factory=FocusAreas)
    severity_config: SeverityConfig = Field(default_factory=SeverityConfig)
    review_settings: ReviewSettings = Field(default_factory=ReviewSettings)
    custom_rules: List[CustomRule] = Field(default_factory=list)
    language_specific: Dict[str, LanguageSpecific] = Field(default_factory=dict)


class Settings(BaseSettings):
    github_token: str
    github_repository: str
    github_pr_number: int
    
    llm_provider: str = "openai"
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_deployment: Optional[str] = None
    gemini_api_key: Optional[str] = None
    
    llm_model: str = "gpt-4-turbo-preview"
    llm_max_tokens: int = 4096
    llm_temperature: float = 0.3
    
    config_file: str = ".ai-review.yaml"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


def load_review_config(config_path: str) -> ReviewConfig:
    if not os.path.exists(config_path):
        return ReviewConfig()
    
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    
    return ReviewConfig(**config_data)


def get_settings() -> Settings:
    return Settings()
