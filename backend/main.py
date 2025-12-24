from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import time
from datetime import datetime

from backend.core.config import settings
from backend.core.logging import setup_logging, logger
from backend.core.monitoring import init_monitoring
from backend.schemas.payloads import HealthCheckResponse

# 1. Setup Logging and Monitoring
setup_logging()
init_monitoring()

# 2. Initialize FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise Multi-Agent Application Server"
)

# 3. Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthCheckResponse, tags=["System"])
async def health_check():
    """System health check endpoint."""
    return HealthCheckResponse(
        status="ok",
        version=settings.VERSION,
        timestamp=datetime.utcnow().isoformat()
    )

# 4. Integrate Agno AgentOS and Routes
from agno.os import AgentOS
from backend.routers.openwebui import router as openwebui_router, workflow as doc_workflow
from backend.routers.admin import router as admin_router
from backend.agents.planner_agent import PlannerAgent
from backend.agents.author_agent import AuthorAgent
from backend.agents.reviewer_agent import ReviewerAgent
from backend.tools.local.enterprise_tools import enterprise_tools

# Initialize Agents for the Tool Server
planner = PlannerAgent()
author = AuthorAgent()
reviewer = ReviewerAgent()

agent_os = AgentOS(
    name="Enterprise MAAS AgentOS",
    description="Orchestrator for Document Creation Agents",
    workflows=[doc_workflow],
    agents=[planner, author, reviewer], # Expose agents
    tools=[enterprise_tools], # Expose specialized enterprise tools
    base_app=app,
)

# Merges AgentOS routes (control plane) with our base app
app = agent_os.get_app()

app.include_router(openwebui_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {settings.PROJECT_NAME} on port {settings.PORT}...")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)
