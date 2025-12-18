from fastapi import APIRouter, Depends
from typing import List
from maas_document_system.app.api_openwebui import JOB_STORE
from maas_document_system.app.middleware.auth import verify_auth

# For now, we reuse the auth middleware, though Admin might need different roles
router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(verify_auth)])

@router.get("/jobs")
async def list_jobs():
    """
    List all jobs for the Admin Dashboard.
    """
    # Convert dict to list
    return list(JOB_STORE.values())

@router.get("/agents")
async def list_agents():
    """
    Get status of agents.
    For MVP, we static return the known agents in the workflow.
    In a real system, we'd query the AgentOS registry or the Workflow instance.
    """
    # Mocking status based on active jobs
    busy = any(j["status"] == "running" for j in JOB_STORE.values())
    status = "busy" if busy else "idle"
    
    return [
        {"id": "agent-planner", "name": "Planner Agent", "role": "Planning", "status": status, "tasks_completed": 10},
        {"id": "agent-author", "name": "Author Agent", "role": "Drafting", "status": status, "tasks_completed": 25},
        {"id": "agent-reviewer", "name": "Reviewer Agent", "role": "Reviewing", "status": status, "tasks_completed": 22},
    ]
