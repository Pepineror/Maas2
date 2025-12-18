from typing import List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class OpenWebUIJobRequest(BaseModel):
    """
    Payload received from OpenWebUI to trigger a document generation job.
    """
    prompt: str = Field(..., description="The user's prompt or description of the document to generate.")
    project_name: Optional[str] = Field(None, description="Inferred project name, if any.")
    template_name: Optional[str] = Field(None, description="Specific template to use.")
    model_name: Optional[str] = Field(None, description="LLM Model to use.")
    user_id: Optional[str] = Field(None, description="User ID from OpenWebUI.")

class OpenWebUIJobResponse(BaseModel):
    """
    Response returned immediately after submitting a job.
    """
    job_id: str = Field(..., description="Unique Job ID.")
    status: str = Field("queued", description="Initial status.")
    message: str = Field("Job submitted successfully.", description="Status message.")
    tracking_url: str = Field(..., description="URL to track job status via WebSocket/Polling.")

class OpenWebUIJobStatus(BaseModel):
    """
    Detailed status schema for polling.
    """
    job_id: str
    status: str = Field(..., description="queued, running, completed, failed")
    progress: int = Field(0, description="0-100 percentage")
    current_step: Optional[str] = Field(None, description="Description of current activity")
    result_url: Optional[str] = Field(None, description="URL to download final document if completed")
    error: Optional[str] = Field(None, description="Error message if failed")
