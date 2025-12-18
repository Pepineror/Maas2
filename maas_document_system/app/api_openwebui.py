from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional
from datetime import datetime
import uuid
import logging

from maas_document_system.schemas.openwebui_requests import OpenWebUIJobRequest, OpenWebUIJobResponse, OpenWebUIJobStatus
from maas_document_system.schemas.project_metadata import ProjectMetadata, ProjectType
# Assuming we will inject the workflow execution logic or use a service
from maas_document_system.workflows.document_creation_workflow import DocumentCreationWorkflow
from maas_document_system.app.middleware.auth import verify_auth
from fastapi import Depends

router = APIRouter(prefix="/openwebui", tags=["OpenWebUI"], dependencies=[Depends(verify_auth)])
logger = logging.getLogger(__name__)

# Simple in-memory job store for MVP/Prototype
# In production this should be Redis or DB
JOB_STORE = {}

workflow = DocumentCreationWorkflow() 

def run_workflow_background(job_id: str, request: OpenWebUIJobRequest):
    """
    Background task wrapper to run the Agno workflow.
    """
    try:
        JOB_STORE[job_id]["status"] = "running"
        JOB_STORE[job_id]["current_step"] = "Initializing workflow"
        
        # Map OpenWebUI request to internal ProjectMetadata
        # Infer project name from prompt if not provided
        proj_name = request.project_name or f"Generated Project {job_id[:8]}"
        
        metadata = ProjectMetadata(
            project_name=proj_name,
            client_name=request.user_id or "OpenWebUI User",
            project_type=ProjectType.OTHER, # We might infer this from prompt analysis agent later
            description=request.prompt,
            template_name=request.template_name,
            priority="normal"
        )
        
        # Execute Workflow
        # Agno workflows are synchronous by default unless configured otherwise or using async runner
        # Creating a plan...
        JOB_STORE[job_id]["current_step"] = "Planning document structure"
        
        # Run workflow
        result = workflow.run(input=metadata, run_id=job_id)
        
        JOB_STORE[job_id]["status"] = "completed"
        JOB_STORE[job_id]["result_url"] = f"/api/v1/downloads/{job_id}"
        JOB_STORE[job_id]["progress"] = 100
        JOB_STORE[job_id]["current_step"] = "Completed"
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        JOB_STORE[job_id]["status"] = "failed"
        JOB_STORE[job_id]["error"] = str(e)

@router.post("/jobs", response_model=OpenWebUIJobResponse)
async def submit_job(request: OpenWebUIJobRequest, background_tasks: BackgroundTasks):
    """
    Submit a new document generation job from OpenWebUI.
    """
    job_id = f"job-{uuid.uuid4()}"
    
    # Initialize Status
    JOB_STORE[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "progress": 0,
        "current_step": "Queued",
        "created_at": datetime.utcnow()
    }
    
    # Hand off to background task
    background_tasks.add_task(run_workflow_background, job_id, request)
    
    return OpenWebUIJobResponse(
        job_id=job_id,
        status="queued",
        message="Job accepted and processing started.",
        tracking_url=f"/openwebui/jobs/{job_id}"
    )

@router.get("/jobs/{job_id}", response_model=OpenWebUIJobStatus)
async def get_job_status(job_id: str):
    """
    Poll status of a specific job.
    """
    job = JOB_STORE.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return OpenWebUIJobStatus(**job)
