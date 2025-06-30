from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_prompt: str
    user_id: str
    conversation_id: str