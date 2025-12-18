from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import Field
import uuid
from maas_document_system.schemas.base import BaseSchema

class AuditAction(str, Enum):
    """Enumeration of allowed audit actions."""
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    GENERATED = "GENERATED"
    ERROR = "ERROR"

class AuditLog(BaseSchema):
    """
    Immutable audit log entry.
    Tracks every significant action within the system for traceability.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the log entry")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Exact time of the event")
    job_id: str = Field(..., description="ID of the job this log belongs to")
    
    actor: str = Field(..., description="Name of the agent or component performing the action")
    action: AuditAction = Field(..., description="Type of action performed")
    target: str = Field(..., description="Target object/section being acted upon")
    
    result: str = Field(..., description="Outcome of the action (e.g., 'Success', 'Failed', 'Approved')")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional context or payload snapshot")

    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "job-123456",
                "actor": "ReviewerAgent",
                "action": "VALIDATED",
                "target": "Section 1.2",
                "result": "Approved",
                "details": {"score": 0.95, "comments": "Looks good."}
            }
        }
