from typing import AsyncGenerator

from app.dto.agent_stream_chunk import AgentStreamChunk
from app.service.base import LLMOrchestratorServiceBase
from app.orchestrator.openai_orchestrator import OpenAIOrchestrator


class LLMOrchestrationService(LLMOrchestratorServiceBase):

    async def generate_response(
        self, user_prompt: str
    ) -> AsyncGenerator[AgentStreamChunk, None]:
        async for chunk in OpenAIOrchestrator().process(user_prompt):
            yield chunk
