from pydantic import BaseModel

from app.dto.db_conversation_record import DbConversationRecord


class ConversationCreateResponse(BaseModel):
    conversation_id: str

def build_from_conversation_record(data: DbConversationRecord):
    return ConversationCreateResponse(conversation_id=str(data.conversation_id))