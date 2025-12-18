from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TemplateSection(BaseModel):
    """
    Represents a section in the document template.
    Usually headers like ## Section Name
    """
    title: str = Field(..., description="Title of the section")
    content: str = Field(..., description="Raw markdown content of the section")
    instructions: Optional[str] = Field(None, description="Specific instructions for this section extracted from comments")

class TemplateMetadata(BaseModel):
    """
    Frontmatter metadata for the template.
    """
    id: str = Field(..., description="Unique identifier for the template")
    name: str = Field(..., description="Human readable name")
    version: str = Field("1.0", description="Template version")
    description: Optional[str] = Field(None, description="Purpose of this template")

class DocumentTemplate(BaseModel):
    """
    Structure of a valid Markdown Template for creating MAAS documents.
    """
    filename: str = Field(..., description="Original filename")
    metadata: Optional[TemplateMetadata] = Field(None, description="Parsed metadata from frontmatter or inference")
    raw_content: str = Field(..., description="Full raw content")
    sections: List[TemplateSection] = Field(default_factory=list, description="Parsed sections")
    
    class Config:
        arbitrary_types_allowed = True
