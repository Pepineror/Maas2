from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class ProjectType(str, Enum):
    BUSINESS_PLAN = "business_plan"
    TECHNICAL_SPEC = "technical_spec"
    MARKETING_STRATEGY = "marketing_strategy"
    OTHER = "other"

class ProjectMetadata(BaseModel):
    project_id: Optional[str] = None
    project_name: str
    client_name: str
    project_type: ProjectType = ProjectType.OTHER
    description: str
    template_name: Optional[str] = None
    priority: str = "normal"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DocumentSection(BaseModel):
    title: str
    heading_level: int = 1
    content: Optional[str] = None
    key_points: List[str] = Field(default_factory=list)
    status: str = "pending" # pending, in_progress, completed

class SectionDecomposition(BaseModel):
    section_title: str
    subsections: List[DocumentSection] = Field(default_factory=list)

class DocumentPlan(BaseModel):
    project_id: str
    title: str
    sections: List[DocumentSection]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class FinalDocument(BaseModel):
    project_id: str
    title: str
    full_text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    file_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ReviewResult(BaseModel):
    """Schema for the output of a review."""
    is_approved: bool = Field(..., description="Whether the content is approved.")
    feedback: str = Field(..., description="Detailed feedback or suggested improvements.")
    score: int = Field(..., description="Quality score from 1-10.")
