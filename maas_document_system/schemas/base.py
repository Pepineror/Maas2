from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
import uuid

class BaseSchema(BaseModel):
    """
    Base Pydantic model for all application schemas.
    Enforces common fields and strict configuration.
    """
    model_config = ConfigDict(
        extra="forbid",
        frozen=True, # Default to immutable, can be overridden if needed
        populate_by_name=True
    )

    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of object creation")
