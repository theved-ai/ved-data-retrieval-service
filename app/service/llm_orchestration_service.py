from typing import AsyncGenerator

from app.service.base import LLMOrchestratorServiceBase
from app.orchestrator.openai_orchestrator import OpenAIOrchestrator


class LLMOrchestrationService(LLMOrchestratorServiceBase):

    def __init__(self):
        self.openai_orchestrator = OpenAIOrchestrator()

    async def generate_response(
        self, user_prompt: str
    ) -> AsyncGenerator[str, None]:
        async for chunk in self.openai_orchestrator.process(user_prompt):
            yield chunk
