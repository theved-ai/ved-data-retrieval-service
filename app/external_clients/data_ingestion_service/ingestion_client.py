import os

import httpx

from app.config.logging_config import logger
from app.decorators.retry_decorator import async_retryable
from app.external_clients.data_ingestion_service.ingestion_payload import IngestionPayload

_INGEST_BASE_URL = os.getenv("INGEST_BASE_URL", "http://localhost:8085")
_INGEST_ENDPOINT = "/v1/ingest"

class IngestionClient:

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or _INGEST_BASE_URL
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=10)

    @async_retryable()
    async def ingest(self, payload: IngestionPayload) -> None:
        logger.debug("Posting chat payload to ingestion service", extra={"payload": payload})
        response = await self._client.post(_INGEST_ENDPOINT, json=payload.model_dump())
        response.raise_for_status()
        logger.debug("Ingestion accepted: %s", response.status_code)

    async def close(self) -> None:
        await self._client.aclose()