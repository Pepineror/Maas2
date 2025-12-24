from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class OpenWebUIJobRequest(BaseModel):
    """Payload received from OpenWebUI via Tool or direct POST"""
    prompt: str
    project_name: Optional[str] = None
    template_name: Optional[str] = None
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class OpenWebUIJobResponse(BaseModel):
    """Response returned to OpenWebUI"""
    job_id: str
    status: str
    message: str
    tracking_url: Optional[str] = None

class OpenWebUIJobStatus(BaseModel):
    """Polling status for OpenWebUI"""
    job_id: str
    status: str
    progress: int = 0
    current_step: str = ""
    result_url: Optional[str] = None
    error: Optional[str] = None

class RedmineProjectContext(BaseModel):
    """Data scraped from Redmine for context"""
    project_id: str
    name: str
    description: Optional[str] = None
    issues: List[Dict[str, Any]] = Field(default_factory=list)
    wiki_content: Optional[str] = None

class HealthCheckResponse(BaseModel):
    status: str = "ok"
    version: str
    timestamp: str
