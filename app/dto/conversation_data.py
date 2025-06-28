from pydantic import BaseModel

class ConversationData(BaseModel):
    conversation_id: str
    title: str