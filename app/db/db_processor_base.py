from abc import abstractmethod, ABC
from typing import Optional

from app.dto.chat_persist_request import ChatPersistRequest
from app.dto.create_conversation import CreateConversation
from app.dto.db_chat_record import DbChatRecord
from app.dto.db_conversation_record import DbConversationRecord
from app.dto.db_model_metadata_record import DbModelMetadataDto


class DbProcessorBase(ABC):

    @abstractmethod
    async def fetch_active_model_metadata_by_category(self, category: str) -> DbModelMetadataDto:
        pass

    @abstractmethod
    async def fetch_conversation_by_id(self, conversation_id: str) -> Optional[DbConversationRecord]:
        pass

    @abstractmethod
    async def insert_conversation(self, req: CreateConversation) -> DbConversationRecord:
        pass

    @abstractmethod
    async def insert_chat(self, req: ChatPersistRequest) -> DbChatRecord:
        pass