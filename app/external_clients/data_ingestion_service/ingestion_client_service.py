from app.dto.db_chat_record import DbChatRecord
from app.external_clients.data_ingestion_service.ingestion_client import IngestionClient
from app.external_clients.data_ingestion_service.ingestion_payload import build_from_chat_data
from app.utils.app_utils import execute_try_catch_async


class IngestionClientService:

    def __init__(self, client: IngestionClient | None = None) -> None:
        self._client = client or IngestionClient()

    async def send_chat_for_ingestion(self, chat_data: DbChatRecord, user_id: str) -> None:
        ingestion_payload = build_from_chat_data(chat_data, user_id)
        await execute_try_catch_async(
            try_fn=lambda: self._client.ingest(ingestion_payload),
            catch_fn=lambda e: RuntimeError(f"Failed to ingest chat payload: {e}")
        )