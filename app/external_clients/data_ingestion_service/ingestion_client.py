import os

import httpx

from app.config.logging_config import logger
from app.decorators.retry_decorator import async_retryable
from app.decorators.try_catch_decorator import try_catch_wrapper
from app.external_clients.data_ingestion_service.ingestion_payload import IngestionPayload
from app.utils.application_constants import ingestion_service_hostname_key, default_ingestion_service_hostname, \
    data_ingestion_endpoint, data_ingestion_error

_INGEST_BASE_URL = os.getenv(ingestion_service_hostname_key, default_ingestion_service_hostname)

class IngestionClient:

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or _INGEST_BASE_URL
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=10)

    @async_retryable()
    @try_catch_wrapper(logger_fn = lambda e: logger.error(data_ingestion_error))
    async def ingest(self, payload: IngestionPayload) -> None:
        logger.debug("Posting chat payload to ingestion service", extra={"payload": payload})
        response = await self._client.post(data_ingestion_endpoint, json=payload.model_dump())
        response.raise_for_status()
        logger.debug("Ingestion accepted: %s", response.status_code)

    async def close(self) -> None:
        await self._client.aclose()