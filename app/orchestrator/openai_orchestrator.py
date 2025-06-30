from typing import AsyncGenerator

from app.ai_agents.mcp_client_agent import MCPClientAgent
from app.decorators.try_catch_decorator import try_catch_wrapper
from app.dto.agent_request import build_agent_req_dto
from app.dto.chat_request import ChatRequest
from app.dto.llm_response_chunk import LlmResponseChunkDto
from app.enums.llm_response_event_type import LlmResponseEventType
from app.orchestrator.llm_orchestrator_base import LLMOrchestratorBase
from app.service.impl.mode_metadata_service import ModelMetadataService
from app.utils.application_constants import default_category, openai_orchestration_failed
from app.config.logging_config import logger


class OpenAIOrchestrator(LLMOrchestratorBase):

    def __init__(self):
        self.mcp_client = MCPClientAgent()
        self.model_metadata_service = ModelMetadataService()

    async def process(self, chat_request: ChatRequest) -> AsyncGenerator[LlmResponseChunkDto, None]:
        model_metadata = await self.model_metadata_service.fetch_model_by_category(default_category)
        yield LlmResponseChunkDto(event_type=LlmResponseEventType.model_metadata_id, data=model_metadata.model_metadata_id)
        streamable_agent_coroutine = self.mcp_client.execute(build_agent_req_dto(model_metadata, chat_request))
        async for chunk in streamable_agent_coroutine:
            yield chunk
