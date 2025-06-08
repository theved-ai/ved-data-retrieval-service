from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from app.dto.agent_stream_chunk import AgentStreamChunk


class LLMOrchestratorBase(ABC):

    @abstractmethod
    async def process(self, user_prompt: str) -> AsyncGenerator[AgentStreamChunk, None]:
        pass
