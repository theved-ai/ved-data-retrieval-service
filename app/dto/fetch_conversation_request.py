from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field

IST = ZoneInfo("Asia/Kolkata")

class FetchConversationRequest(BaseModel):
    user_id: str
    max_conversation_limit: int
    search_text: str
    last_conversation_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(IST)
    )