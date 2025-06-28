from enum import Enum


class LlmResponseEventType(Enum):
    tool_call_list='tool_call_list'
    raw_response='raw_response'
    model_metadata_id='model_metadata_id'