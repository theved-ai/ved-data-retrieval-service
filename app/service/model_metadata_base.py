from abc import ABC, abstractmethod

from app.dto.model_metadata import ModelMetadataDto


class ModelMetadataBase(ABC):

    @abstractmethod
    def fetch_model_by_category(self, category: str) -> ModelMetadataDto:
        pass