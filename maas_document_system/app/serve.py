from fastapi import FastAPI
from agno.os import AgentOS
from maas_document_system.workflows.document_creation_workflow import DocumentCreationWorkflow

# 1. Define the FastAPI app (optional, AgentOS can create one)
app = FastAPI(
    title="MAAS Document System",
    description="Multi-Agent Application Server for Document Generation",
    version="1.0.0"
)

from maas_document_system.app.api_openwebui import router as openwebui_router
from maas_document_system.app.api_admin import router as admin_router
app.include_router(openwebui_router)
app.include_router(admin_router)

# 2. Instantiate Workflows
# AgentOS will manage the routes and execution for these workflows
doc_workflow = DocumentCreationWorkflow()

# 3. Instantiate AgentOS
# This is the Control Plane integration point
agent_os = AgentOS(
    name="MAAS AgentOS",
    description="Orchestrator for Document Creation Agents",
    workflows=[doc_workflow],
    base_app=app,  # Helper to mount on existing app
    auto_provision_dbs=True, # For MVP using default if needed
)

# 4. Get the final app
# This merges AgentOS routes with the base app
app = agent_os.get_app()

if __name__ == "__main__":
    # Development server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
