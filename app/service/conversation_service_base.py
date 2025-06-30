from abc import ABC, abstractmethod

from app.dto.conversation_create_response import ConversationCreateResponse
from app.dto.conversation_fetch_response import ConversationFetchResponse
from app.dto.create_conversation import CreateConversation
from app.dto.fetch_conversation_request import FetchConversationRequest


class ConversationServiceBase(ABC):

    @abstractmethod
    def create_conversation(self, req: CreateConversation) -> ConversationCreateResponse:
        pass

    @abstractmethod
    async def does_conversation_exist(self, conversation_id: str) -> bool:
        pass

    @abstractmethod
    def fetch_conversations(self, req: FetchConversationRequest) -> ConversationFetchResponse:
        pass