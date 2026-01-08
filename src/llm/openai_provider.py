from typing import Dict, Any
from openai import AsyncOpenAI
from .base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview", 
                 temperature: float = 0.3, max_tokens: int = 4096):
        super().__init__(model, temperature, max_tokens)
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def generate_review(self, prompt: str, context: Dict[str, Any]) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert code reviewer. Provide detailed, actionable feedback on code quality, security, performance, and best practices."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def estimate_tokens(self, text: str) -> int:
        return len(text) // 4
