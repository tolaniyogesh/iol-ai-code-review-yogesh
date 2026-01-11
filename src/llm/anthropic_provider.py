from typing import Dict, Any
from anthropic import AsyncAnthropic
from .base import BaseLLMProvider


class AnthropicProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229",
                 temperature: float = 0.3, max_tokens: int = 4096):
        super().__init__(model, temperature, max_tokens)
        self.client = AsyncAnthropic(api_key=api_key)
    
    async def generate_review(self, prompt: str, context: Dict[str, Any]) -> str:
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system="You are an expert code reviewer. Provide detailed, actionable feedback on code quality, security, performance, and best practices.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    def estimate_tokens(self, text: str) -> int:
        return len(text) // 4
