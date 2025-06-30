import asyncio

from app.config.logging_config import logger
from app.db.postgres.postgres_processor import PostgresProcessor
from app.decorators.try_catch_decorator import try_catch_wrapper
from app.dto.bulk_chat_response import BulkChatResponse
from app.dto.chat_data import build_from_chat_record
from app.dto.chat_fetch_request import ChatFetchRequestDto
from app.dto.chat_persist_request import ChatPersistRequest
from app.external_clients.data_ingestion_service.ingestion_client_service import IngestionClientService
from app.service.chat_service_base import ChatServiceBase
from app.utils.application_constants import saving_chat_service_error


class ChatService(ChatServiceBase):

    def __init__(self):
        self.storage_service = PostgresProcessor()
        self.ingestion_service = IngestionClientService()

    @try_catch_wrapper(logger_fn = lambda e: logger.error(saving_chat_service_error))
    async def save_chat(self, req: ChatPersistRequest):
        chat_record = await self.storage_service.insert_chat(req)
        task=asyncio.create_task(self.ingestion_service.send_chat_for_ingestion(chat_record, req.user_id))
        return build_from_chat_record(chat_record)

    def fetch_chats(self, req: ChatFetchRequestDto) -> BulkChatResponse:
        pass