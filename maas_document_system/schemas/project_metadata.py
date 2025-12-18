from datetime import datetime
from typing import Dict, Optional, List
from enum import Enum
from pydantic import Field, HttpUrl
from maas_document_system.schemas.base import BaseSchema

class ProjectType(str, Enum):
    RESEARCH_REPORT = "research_report"
    VIABILITY_STUDY = "viability_study"
    TECHNICAL_SPEC = "technical_spec"
    OTHER = "other"

class ProjectMetadata(BaseSchema):
    """
    Defines the metadata required to initialize a document generation job.
    This schema serves as the contract for the input data provided by OpenWebUI.
    """
    project_name: str = Field(..., description="Name of the project or document to be generated", min_length=3)
    client_name: str = Field(..., description="Name of the client requesting the document")
    project_type: ProjectType = Field(..., description="Type of document")
    
    # Optional parameters for added context
    description: Optional[str] = Field(None, description="Brief description of the project scope")
    tags: List[str] = Field(default_factory=list, description="List of tags for categorizations")
    
    # Constraints and rules
    priority: str = Field("normal", description="Priority level: 'low', 'normal', 'high'")
    callback_url: Optional[HttpUrl] = Field(None, description="Webhook URL for status updates")
    template_name: Optional[str] = Field(None, description="Filename of the markdown template to use (e.g. 'Plantilla para SIC 01.md')")

    class Config:
        json_schema_extra = {
            "example": {
                "project_name": "Metro Line 3 Viability",
                "client_name": "City Council",
                "project_type": "viability_study",
                "description": "Comprehensive viability study for the new metro line extension.",
                "tags": ["infrastructure", "transport"],
                "priority": "high"
            }
        }
