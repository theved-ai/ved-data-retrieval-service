from app.config.logging_config import logger
from app.decorators.try_catch_decorator import try_catch_wrapper
from app.dto.db_chat_record import DbChatRecord
from app.external_clients.data_ingestion_service.ingestion_client import IngestionClient
from app.external_clients.data_ingestion_service.ingestion_payload import build_from_chat_data
from app.utils.application_constants import data_ingestion_service_error


class IngestionClientService:

    def __init__(self, client: IngestionClient | None = None) -> None:
        self._client = client or IngestionClient()

    @try_catch_wrapper(logger_fn= lambda e: logger.exception(data_ingestion_service_error))
    async def send_chat_for_ingestion(self, chat_data: DbChatRecord, user_id: str) -> None:
        ingestion_payload = build_from_chat_data(chat_data, user_id)
        await self._client.ingest(ingestion_payload)