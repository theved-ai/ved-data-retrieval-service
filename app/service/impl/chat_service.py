from app.db.postgres.postgres_processor import PostgresProcessor
from app.dto.bulk_chat_response import BulkChatResponse
from app.dto.chat_data_dto import build_from_chat_record
from app.dto.chat_fetch_request_dto import ChatFetchRequestDto
from app.dto.chat_persist_request_dto import ChatPersistRequest
from app.service.chat_service_base import ChatServiceBase
from app.utils.app_utils import execute_try_catch_async


class ChatService(ChatServiceBase):

    def __init__(self):
        self.storage_service = PostgresProcessor()

    async def save_chat(self, req: ChatPersistRequest):
        chat_record = await execute_try_catch_async(
            lambda: self.storage_service.insert_chat(req),
            lambda e: RuntimeError(f'Exception while saving chat: {req}')
        )
        return build_from_chat_record(chat_record)

    def fetch_chats(self, req: ChatFetchRequestDto) -> BulkChatResponse:
        pass