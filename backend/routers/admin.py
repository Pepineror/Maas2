from fastapi import APIRouter, Depends
from typing import List
from backend.routers.openwebui import JOB_STORE
from backend.middleware.auth import verify_auth

# For now, we reuse the auth middleware, though Admin might need different roles
router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(verify_auth)])

@router.get("/jobs")
async def list_jobs():
    """
    List all jobs for the Admin Dashboard.
    """
    # Convert dict to list
    return list(JOB_STORE.values())

@router.get("/jobs/{job_id}")
async def get_job_details(job_id: str):
    """Get full details of a specific job."""
    job = JOB_STORE.get(job_id)
    if not job:
        return {"error": "Job not found"}
    return job

@router.post("/cache/clear")
async def clear_cache():
    """Clear the RealTimeCache (Redis)."""
    from backend.core.redis_client import redis_client
    if redis_client.client:
        redis_client.client.flushdb()
        return {"status": "success", "message": "Cache cleared."}
    return {"status": "error", "message": "Redis not connected."}

@router.get("/agents")
async def list_agents():
    """Get status of agents."""
    busy = any(j["status"] == "running" for j in JOB_STORE.values())
    status = "busy" if busy else "idle"
    
    return [
        {"id": "agent-planner", "name": "Planner Agent", "role": "Planning", "status": status, "tasks_completed": 10},
        {"id": "agent-author", "name": "Author Agent", "role": "Drafting", "status": status, "tasks_completed": 25},
        {"id": "agent-reviewer", "name": "Reviewer Agent", "role": "Reviewing", "status": status, "tasks_completed": 22},
    ]
