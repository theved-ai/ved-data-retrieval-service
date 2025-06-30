from pydantic import BaseModel

class ChatResponse(BaseModel):
    message_id: str
    response_content: str