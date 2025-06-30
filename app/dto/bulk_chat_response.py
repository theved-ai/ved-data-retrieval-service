from datetime import datetime

from pydantic import BaseModel

from app.dto.chat_data import ChatDataDto


class BulkChatResponse(BaseModel):
    latest_message_at: datetime
    oldest_message_at: datetime
    conversation_id: str
    messages: list[ChatDataDto]