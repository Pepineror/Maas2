from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import Dict, Any
from datetime import datetime
import uuid
import logging

from backend.schemas.payloads import OpenWebUIJobRequest, OpenWebUIJobResponse, OpenWebUIJobStatus
from backend.schemas.models import ProjectMetadata, ProjectType
from backend.workflows.document_creation_workflow import DocumentCreationWorkflow

router = APIRouter(prefix="/openwebui", tags=["OpenWebUI"])
logger = logging.getLogger(__name__)

# Singleton workflow instance
workflow = DocumentCreationWorkflow()

# In-memory store for MVP. In production, use Redis/DB via backend.core.config
JOB_STORE: Dict[str, Any] = {}

async def run_workflow_background(job_id: str, request: OpenWebUIJobRequest):
    """
    Background task to execute the document creation workflow.
    """
    try:
        JOB_STORE[job_id]["status"] = "running"
        JOB_STORE[job_id]["current_step"] = "Planning"
        
        # Map request to internal metadata
        metadata = ProjectMetadata(
            project_id=job_id,
            project_name=request.project_name or f"Job {job_id[:8]}",
            client_name=request.user_id or "OpenWebUI User",
            project_type=ProjectType.OTHER,
            description=request.prompt,
            template_name=request.template_name
        )
        
        # Execute Workflow
        result = workflow.run(input=metadata, run_id=job_id)
        
        JOB_STORE[job_id]["status"] = "completed"
        JOB_STORE[job_id]["progress"] = 100
        JOB_STORE[job_id]["current_step"] = "Document generated successfully"
        JOB_STORE[job_id]["result_url"] = f"/api/v1/downloads/{job_id}"
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        JOB_STORE[job_id]["status"] = "failed"
        JOB_STORE[job_id]["error"] = str(e)

@router.post("/jobs", response_model=OpenWebUIJobResponse)
async def submit_job(request: OpenWebUIJobRequest, background_tasks: BackgroundTasks):
    """Submit a new job from OpenWebUI."""
    job_id = f"job-{uuid.uuid4()}"
    
    JOB_STORE[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "progress": 0,
        "current_step": "Queued",
        "created_at": datetime.utcnow()
    }
    
    background_tasks.add_task(run_workflow_background, job_id, request)
    
    return OpenWebUIJobResponse(
        job_id=job_id,
        status="queued",
        message="Job accepted.",
        tracking_url=f"/api/v1/openwebui/jobs/{job_id}"
    )

@router.get("/jobs/{job_id}", response_model=OpenWebUIJobStatus)
async def get_job_status(job_id: str):
    """Poll job status."""
    job = JOB_STORE.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return OpenWebUIJobStatus(**job)
