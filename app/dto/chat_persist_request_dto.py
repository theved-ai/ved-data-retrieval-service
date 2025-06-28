from pydantic import BaseModel

class ChatPersistRequest(BaseModel):
    user_id: str
    conversation_id: str
    content: dict[str, str]
    tools_called: list[str]
    model_metadata_id: int