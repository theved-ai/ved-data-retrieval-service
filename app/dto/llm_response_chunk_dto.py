from typing import Any

from pydantic import BaseModel

from app.enums.llm_response_event_type import LlmResponseEventType


class LlmResponseChunkDto(BaseModel):
    event_type: LlmResponseEventType
    data: Any