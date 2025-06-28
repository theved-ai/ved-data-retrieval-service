from datetime import datetime

from pydantic import BaseModel

from app.dto.conversation_data import ConversationData


class ConversationFetchResponse(BaseModel):
    user_id: str
    latest_conversation_at: datetime
    oldest_conversation_at: datetime
    conversations: list[ConversationData]