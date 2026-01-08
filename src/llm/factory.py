from typing import Optional
from .base import BaseLLMProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .azure_provider import AzureOpenAIProvider
from .gemini_provider import GeminiProvider


class LLMProviderFactory:
    @staticmethod
    def create_provider(
        provider: str,
        model: str,
        temperature: float = 0.3,
        max_tokens: int = 4096,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
        azure_openai_api_key: Optional[str] = None,
        azure_openai_endpoint: Optional[str] = None,
        azure_openai_deployment: Optional[str] = None,
        gemini_api_key: Optional[str] = None
    ) -> BaseLLMProvider:
        provider = provider.lower()
        
        if provider == "openai":
            if not openai_api_key:
                raise ValueError("OpenAI API key is required")
            return OpenAIProvider(
                api_key=openai_api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
        
        elif provider == "anthropic":
            if not anthropic_api_key:
                raise ValueError("Anthropic API key is required")
            return AnthropicProvider(
                api_key=anthropic_api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
        
        elif provider == "azure":
            if not all([azure_openai_api_key, azure_openai_endpoint, azure_openai_deployment]):
                raise ValueError("Azure OpenAI credentials are required")
            return AzureOpenAIProvider(
                api_key=azure_openai_api_key,
                endpoint=azure_openai_endpoint,
                deployment=azure_openai_deployment,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
        
        elif provider == "gemini":
            if not gemini_api_key:
                raise ValueError("Gemini API key is required")
            return GeminiProvider(
                api_key=gemini_api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
        
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
