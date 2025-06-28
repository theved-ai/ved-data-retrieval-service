from app.db.postgres.postgres_processor import PostgresProcessor
from app.dto.conversation_create_response import ConversationCreateResponse, build_from_conversation_record
from app.dto.conversation_fetch_response import ConversationFetchResponse
from app.dto.create_conversation_dto import CreateConversation
from app.dto.fetch_conversation_request import FetchConversationRequest
from app.service.conversation_service_base import ConversationServiceBase
from app.utils.app_utils import execute_if_or_else


class ConversationService(ConversationServiceBase):

    def __init__(self):
        self.storage_service = PostgresProcessor()

    async def create_conversation(self, req: CreateConversation) -> ConversationCreateResponse:
        conversation_record = await self.storage_service.insert_conversation(req)
        return build_from_conversation_record(conversation_record)

    async def does_conversation_exist(self, conversation_id: str) -> bool:
        return execute_if_or_else(
            await self.storage_service.fetch_conversation_by_id(conversation_id) is not None,
            lambda: True,
            lambda: False
        )

    async def fetch_conversations(self, req: FetchConversationRequest) -> ConversationFetchResponse:
        pass