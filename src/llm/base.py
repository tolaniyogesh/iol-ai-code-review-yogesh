from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseLLMProvider(ABC):
    def __init__(self, model: str, temperature: float = 0.3, max_tokens: int = 4096):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    @abstractmethod
    async def generate_review(self, prompt: str, context: Dict[str, Any]) -> str:
        pass
    
    @abstractmethod
    def estimate_tokens(self, text: str) -> int:
        pass
    
    def truncate_to_token_limit(self, text: str, max_tokens: int) -> str:
        estimated = self.estimate_tokens(text)
        if estimated <= max_tokens:
            return text
        
        ratio = max_tokens / estimated
        target_length = int(len(text) * ratio * 0.9)
        return text[:target_length] + "\n... [truncated]"
