from abc import ABC, abstractmethod
from typing import AsyncGenerator

from app.dto.agent_request_dto import AgentRequestDto


class AgentBase(ABC):

    @abstractmethod
    async def execute(
        self, req: AgentRequestDto
    ) -> AsyncGenerator[str, None]:
        pass
