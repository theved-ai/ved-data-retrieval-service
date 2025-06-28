from app.db.postgres.postgres_processor import PostgresProcessor
from app.dto.model_metadata_dto import ModelMetadataDto
from app.service.model_metadata_base import ModelMetadataBase


class ModelMetadataService(ModelMetadataBase):

    def __init__(self):
        self.storage_service = PostgresProcessor()

    async def fetch_model_by_category(self, category: str) -> ModelMetadataDto:
        model_metadata_record = await self.storage_service.fetch_active_model_metadata_by_category(category)
        return ModelMetadataDto(
            model_metadata_id = model_metadata_record.model_metadata_id,
            model_name = model_metadata_record.model_name,
            model_instruction = model_metadata_record.model_instruction
        )