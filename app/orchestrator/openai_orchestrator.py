from typing import AsyncGenerator

from app.dto.agent_request_dto import AgentRequestDto
from app.orchestrator.base import LLMOrchestratorBase
from app.agents.mcp_client_agent import MCPClientAgent


class OpenAIOrchestrator(LLMOrchestratorBase):

    async def process(self, user_prompt: str) -> AsyncGenerator[str, None]:
        async for chunk in MCPClientAgent().execute(req=AgentRequestDto(user_prompt)):
            yield chunk
