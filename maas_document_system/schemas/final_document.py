from typing import Optional, List
from pydantic import Field
from datetime import datetime
import uuid
from maas_document_system.schemas.base import BaseSchema

class FinalDocument(BaseSchema):
    """
    Represents the final consolidated output of the generation process.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique document ID")
    job_id: str = Field(..., description="Reference to the job")
    
    # Materialized file paths
    pdf_path: Optional[str] = Field(None, description="Absolute path to the final PDF")
    docx_path: Optional[str] = Field(None, description="Absolute path to the final DOCX")
    markdown_path: Optional[str] = Field(None, description="Absolute path to the consolidated Markdown")
    
    # Stats
    total_sections: int = Field(..., description="Total number of sections included")
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    
    checksum_sha256: Optional[str] = Field(None, description="Hash of the final output for integrity")

    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "job-123",
                "pdf_path": "/outputs/job-123/final.pdf",
                "total_sections": 15
            }
        }
