from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class DbModelMetadataDto(BaseModel):
    model_metadata_id: int
    model_name: str
    model_instruction: str
    category: str
    model_configuration: Optional[dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = 'ignore'