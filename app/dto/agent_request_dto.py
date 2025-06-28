from pydantic import BaseModel

from app.dto.chat_request_dto import ChatRequest
from app.dto.model_metadata_dto import ModelMetadataDto


def build_agent_req_dto(model_metadata: ModelMetadataDto, chat_request: ChatRequest):
    return AgentRequestDto(
        user_prompt=chat_request.user_prompt,
        user_id=chat_request.user_id,
        model_metadata=model_metadata
    )


class AgentRequestDto(BaseModel):
    user_prompt: str
    model_metadata: ModelMetadataDto
    user_id: str

