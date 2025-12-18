from typing import List, Optional
from pydantic import Field
import uuid
from datetime import datetime
from maas_document_system.schemas.base import BaseSchema

class PlanItem(BaseSchema):
    """
    Represents a planned item in the document structure.
    Lightweight representation for the plan.
    """
    section_id: str = Field(..., description="Pre-generated ID for the section")
    title: str = Field(..., description="Proposed title")
    description_prompt: str = Field(..., description="Prompt/instruction for the author agent")
    hierarchy_level: int = Field(..., description="Hierarchy level")
    order_index: int = Field(..., description="Position in the document linear flow")

class DocumentPlan(BaseSchema):
    """
    Defines the structural plan of the document to be generated.
    Produced by the PlannerAgent.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique plan ID")
    job_id: str = Field(..., description="Reference to the parent job")
    
    outline: List[PlanItem] = Field(..., description="Ordered list of sections to be generated")
    
    version: str = Field("1.0", description="Plan version")

    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "job-123",
                "outline": [
                    {
                        "section_id": "sec-1",
                        "title": "Introduction",
                        "description_prompt": "Write an intro summarizing the project.",
                        "hierarchy_level": 1,
                        "order_index": 0
                    }
                ]
            }
        }
