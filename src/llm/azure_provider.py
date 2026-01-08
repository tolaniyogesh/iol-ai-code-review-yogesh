from typing import Dict, Any
from openai import AsyncAzureOpenAI
from .base import BaseLLMProvider


class AzureOpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, endpoint: str, deployment: str,
                 model: str = "gpt-4", temperature: float = 0.3, max_tokens: int = 4096):
        super().__init__(model, temperature, max_tokens)
        self.client = AsyncAzureOpenAI(
            api_key=api_key,
            api_version="2024-02-15-preview",
            azure_endpoint=endpoint
        )
        self.deployment = deployment
    
    async def generate_review(self, prompt: str, context: Dict[str, Any]) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.deployment,
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
            raise Exception(f"Azure OpenAI API error: {str(e)}")
    
    def estimate_tokens(self, text: str) -> int:
        return len(text) // 4
