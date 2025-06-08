from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from app.dto.agent_stream_chunk import AgentStreamChunk


class LLMOrchestratorServiceBase(ABC):

    @abstractmethod
    async def generate_response(
        self, user_prompt: str
    ) -> AsyncGenerator[AgentStreamChunk, None]:
        pass
