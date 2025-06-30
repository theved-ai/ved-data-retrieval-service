from datetime import datetime

from pydantic import BaseModel

class ChatFetchRequestDto(BaseModel):
    conversation_id: str
    last_message_at: datetime
    message_limit: int