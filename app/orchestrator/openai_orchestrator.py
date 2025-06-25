from typing import AsyncGenerator

from app.agents.mcp_client_agent import MCPClientAgent
from app.dto.agent_request_dto import AgentRequestDto
from app.orchestrator.base import LLMOrchestratorBase

USER_UUID = "7dcb16b8-c05c-4ec4-9524-0003e11acd2a"

class OpenAIOrchestrator(LLMOrchestratorBase):

    def __init__(self, user_uuid: str = USER_UUID):
        self.mcp_client = MCPClientAgent(user_uuid)

    async def process(self, user_prompt: str) -> AsyncGenerator[str, None]:
        async for chunk in self.mcp_client.execute(req=AgentRequestDto(user_prompt)):
            yield chunk
