import asyncio
import sys
from src.config import get_settings, load_review_config
from src.github_client import GitHubClient
from src.llm.factory import LLMProviderFactory
from src.reviewer import CodeReviewer
from src.logger import setup_logger

logger = setup_logger(__name__)


async def main():
    try:
        logger.info("Starting AI Code Review Assistant")
        
        settings = get_settings()
        logger.info(f"Loaded settings for repository: {settings.github_repository}")
        
        config = load_review_config(settings.config_file)
        logger.info(f"Loaded review configuration from {settings.config_file}")
        
        github_client = GitHubClient(
            token=settings.github_token,
            repository=settings.github_repository
        )
        logger.info("GitHub client initialized")
        
        llm_provider = LLMProviderFactory.create_provider(
            provider=settings.llm_provider,
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
            openai_api_key=settings.openai_api_key,
            anthropic_api_key=settings.anthropic_api_key,
            azure_openai_api_key=settings.azure_openai_api_key,
            azure_openai_endpoint=settings.azure_openai_endpoint,
            azure_openai_deployment=settings.azure_openai_deployment,
            gemini_api_key=settings.gemini_api_key
        )
        logger.info(f"LLM provider initialized: {settings.llm_provider}")
        
        reviewer = CodeReviewer(
            github_client=github_client,
            llm_provider=llm_provider,
            config=config
        )
        
        result = await reviewer.review_pull_request(settings.github_pr_number)
        
        logger.info(f"Review completed: {result}")
        
        if result.get('should_block'):
            logger.warning("PR should be blocked due to critical issues")
            sys.exit(1)
        
        logger.info("Review completed successfully")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Review failed with error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
