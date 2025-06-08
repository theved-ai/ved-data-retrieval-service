from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

class LLMOrchestratorBase(ABC):

    @abstractmethod
    async def process(self, user_prompt: str) -> AsyncGenerator[str, None]:
        pass
