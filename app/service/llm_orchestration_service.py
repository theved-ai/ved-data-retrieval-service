from typing import AsyncGenerator

from app.service.base import LLMOrchestratorServiceBase
from app.orchestrator.openai_orchestrator import OpenAIOrchestrator


class LLMOrchestrationService(LLMOrchestratorServiceBase):

    async def generate_response(
        self, user_prompt: str
    ) -> AsyncGenerator[str, None]:
        async for chunk in OpenAIOrchestrator().process(user_prompt):
            yield chunk
