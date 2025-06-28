from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from app.dto.chat_request_dto import ChatRequest


class LLMOrchestratorServiceBase(ABC):

    @abstractmethod
    async def generate_response(self, chat_request: ChatRequest) -> AsyncGenerator[str, None]:
        pass
