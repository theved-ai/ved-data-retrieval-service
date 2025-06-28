from typing import AsyncGenerator

from app.ai_agents.mcp_client_agent import MCPClientAgent
from app.dto.agent_request_dto import build_agent_req_dto
from app.dto.chat_request_dto import ChatRequest
from app.dto.llm_response_chunk_dto import LlmResponseChunkDto
from app.enums.llm_response_event_type import LlmResponseEventType
from app.orchestrator.base import LLMOrchestratorBase
from app.service.impl.mode_metadata_service import ModelMetadataService
from app.utils.application_constants import default_category


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
