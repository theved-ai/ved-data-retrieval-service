from abc import ABC, abstractmethod

from app.dto.bulk_chat_response import BulkChatResponse
from app.dto.chat_data_dto import ChatDataDto
from app.dto.chat_fetch_request_dto import ChatFetchRequestDto
from app.dto.chat_persist_request_dto import ChatPersistRequest


class ChatServiceBase(ABC):

    @abstractmethod
    async def save_chat(self, req: ChatPersistRequest) -> ChatDataDto:
        pass

    @abstractmethod
    async def fetch_chats(self, req: ChatFetchRequestDto) -> BulkChatResponse:
        pass