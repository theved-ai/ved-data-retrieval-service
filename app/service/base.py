from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

class LLMOrchestratorServiceBase(ABC):

    @abstractmethod
    async def generate_response(
        self, user_prompt: str
    ) -> AsyncGenerator[str, None]:
        pass
