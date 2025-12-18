from enum import Enum
from typing import Optional, List
from pydantic import Field
from datetime import datetime
import uuid
from maas_document_system.schemas.base import BaseSchema

class SectionStatus(str, Enum):
    """Status lifecycle of a document section."""
    PLANNED = "PLANNED"
    DRAFTING = "DRAFTING"
    DRAFTED = "DRAFTED"
    REVIEWING = "REVIEWING"
    REVIEWED = "REVIEWED" # Successfully validated
    FAILED_VALIDATION = "FAILED_VALIDATION" # Transitory failure
    FAILED_FINAL = "FAILED_FINAL" # Terminal failure after retries
    SKIPPED = "SKIPPED"

class SectionContent(BaseSchema):
    """
    Represents the content and state of a single section within the document.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the section")
    plan_id: str = Field(..., description="ID of the document plan this section belongs to")
    
    title: str = Field(..., description="Title of the section")
    hierarchy_level: int = Field(1, ge=1, description="Heading level (1=H1, 2=H2, etc.)")
    
    content_md: Optional[str] = Field(None, description="Generated content in Markdown format")
    
    status: SectionStatus = Field(SectionStatus.PLANNED, description="Current execution status of the section")
    validation_attempts: int = Field(0, ge=0, description="Count of validation failures/retries")
    
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of last modification")
    error_message: Optional[str] = Field(None, description="Last error message if in failed state")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "2.1 Technical Analysis",
                "hierarchy_level": 2,
                "content_md": "## 2.1 Technical Analysis\n\nThe preliminary analysis shows...",
                "status": "DRAFTED",
                "validation_attempts": 1
            }
        }
