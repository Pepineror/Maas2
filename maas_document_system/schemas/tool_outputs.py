from typing import Dict, Any, Optional
from pydantic import Field
from maas_document_system.schemas.base import BaseSchema

class ViabilityMetrics(BaseSchema):
    """Output schema for Viability Data tool."""
    project_name: str = Field(..., description="Project name queried")
    roi_estimate: float = Field(..., description="Estimated ROI percentage")
    viability_score: int = Field(..., ge=0, le=100, description="0-100 Viability Score")
    risk_level: str = Field(..., description="Risk assessment: Low, Medium, High")
    
    details: Dict[str, Any] = Field(default_factory=dict, description="Raw data payload")

class SourceContent(BaseSchema):
    """Output schema for Source Fetching tool."""
    source_id: str = Field(..., description="Input source ID")
    content_text: str = Field(..., description="Extracted text content")
    sha256_hash: str = Field(..., description="Content hash for change detection")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Source metadata (author, date, etc.)")

class RenderOutput(BaseSchema):
    """Output schema for PDF Rendering tool."""
    output_path: str = Field(..., description="Absolute path to generated file")
    format: str = Field("pdf", description="Output format")
    size_bytes: int = Field(..., description="File size in bytes")
    pages: int = Field(..., description="Number of pages generated")
