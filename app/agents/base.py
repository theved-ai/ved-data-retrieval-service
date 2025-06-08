from abc import ABC, abstractmethod
from typing import AsyncGenerator

from app.dto.agent_request_dto import AgentRequestDto
from app.dto.agent_stream_chunk import AgentStreamChunk


class AgentBase(ABC):

    @abstractmethod
    async def execute(
        self, req: AgentRequestDto
    ) -> AsyncGenerator[AgentStreamChunk, None]:
        pass
