from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class DbConversationRecord(BaseModel):
    conversation_id: UUID
    user_id: UUID
    title: str
    created_at: datetime
    last_message_at: datetime