from typing import Optional

from pydantic import BaseModel, Field

class CreateConversation(BaseModel):
    user_id: str
    title: Optional[str] = Field(
        default_factory=lambda: 'default'
    )