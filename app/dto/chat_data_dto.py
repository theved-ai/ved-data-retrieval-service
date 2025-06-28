import json

from pydantic import BaseModel

from app.dto.db_chat_record import DbChatRecord


class ChatDataDto(BaseModel):
    user_prompt: str
    model_response: str
    message_id: str

def build_from_chat_record(data: DbChatRecord):
    content_json = json.loads(data.content)
    return ChatDataDto(
        user_prompt=content_json.get('user_prompt'),
        model_response=content_json.get('system_response'),
        message_id=str(data.message_id)
    )