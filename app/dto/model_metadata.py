from pydantic import BaseModel

class ModelMetadataDto(BaseModel):
    model_metadata_id: int
    model_name: str
    model_instruction: str
