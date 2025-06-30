from typing import AsyncGenerator

from app.dto.chat_request import ChatRequest
from app.dto.llm_response_chunk import LlmResponseChunkDto
from app.orchestrator.openai_orchestrator import OpenAIOrchestrator
from app.service.impl.conversation_service import ConversationService
from app.service.llm_orchestrator_base import LLMOrchestratorServiceBase
from app.utils.app_utils import ensure_async
from app.utils.application_constants import conversation_not_exist


class LLMOrchestrationService(LLMOrchestratorServiceBase):

    def __init__(self):
        self.openai_orchestrator = OpenAIOrchestrator()
        self.conversation_service = ConversationService()

    async def generate_response(self, chat_request: ChatRequest) -> AsyncGenerator[LlmResponseChunkDto, None]:
        await ensure_async(
            lambda: self.conversation_service.does_conversation_exist(chat_request.conversation_id),
            conversation_not_exist.format(conversation_id=chat_request.conversation_id)
        )
        async for chunk in self.openai_orchestrator.process(chat_request):
            yield chunk
