from abc import ABC, abstractmethod

from app.dto.model_metadata_dto import ModelMetadataDto


class ModelMetadataBase(ABC):

    @abstractmethod
    def fetch_model_by_category(self, category: str) -> ModelMetadataDto:
        pass