from typing import Dict, Any
import google.generativeai as genai
from .base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash",
                 temperature: float = 0.3, max_tokens: int = 4096):
        super().__init__(model, temperature, max_tokens)
        genai.configure(api_key=api_key)
        self.model_instance = genai.GenerativeModel(model)
        
        self.generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
    
    async def generate_review(self, prompt: str, context: Dict[str, Any]) -> str:
        try:
            system_instruction = "You are an expert code reviewer. Provide detailed, actionable feedback on code quality, security, performance, and best practices."
            
            full_prompt = f"{system_instruction}\n\n{prompt}"
            
            response = await self.model_instance.generate_content_async(
                full_prompt,
                generation_config=self.generation_config
            )
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def estimate_tokens(self, text: str) -> int:
        return self.model_instance.count_tokens(text).total_tokens
