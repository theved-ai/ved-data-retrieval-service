import json
from typing import Any, Dict
from pydantic import BaseModel
from app.utils.application_constants import chat_ingest_input_source
from app.dto.db_chat_record import DbChatRecord


class IngestionPayload(BaseModel):
    user_id: str
    data_source: str = chat_ingest_input_source
    content: str
    metadata: Dict[str, Any]

def build_from_chat_data(data: DbChatRecord, user_id: str):
    return IngestionPayload(
        user_id=user_id,
        content=json.loads(data.content).get('user_prompt'),
        metadata={
            'conversation_id': str(data.conversation_id),
            'message_id': str(data.message_id)
        }
    )