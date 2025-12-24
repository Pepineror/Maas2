from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class ViabilityMetrics(BaseModel):
    project_name: str
    roi_estimate: float
    viability_score: int
    risk_level: str
    details: Dict[str, Any] = Field(default_factory=dict)

class SourceContent(BaseModel):
    source_id: str
    content_text: str
    sha256_hash: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SectionContent(BaseModel):
    project_id: str
    title: str
    content_md: str
    status: str = "drafted"
    metadata: Dict[str, Any] = Field(default_factory=dict)
