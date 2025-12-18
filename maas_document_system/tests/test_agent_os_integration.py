from fastapi.testclient import TestClient
from maas_document_system.app.serve import app
import pytest
import os

@pytest.fixture(autouse=True)
def ensure_no_api_key():
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

def test_agent_os_routes_exist():
    client = TestClient(app)
    
    # List all routes to help debugging
    routes = [route.path for route in app.routes]
    print(f"\nALL ROUTES:\n" + "\n".join(routes) + "\n")
    
    # Check if standard AgentOS routes are present
    assert "/health" in routes
    
    # Check if our workflow is exposed
    # Agno usually exposes workflows at /workflows/{name}/run or similar
    # The name in workflow is "Document Creation Workflow", id might be "document-creation-workflow"
    
    workflow_routes = [r for r in routes if "workflows" in r]
    print(f"WORKFLOW ROUTES: {workflow_routes}")
    assert len(workflow_routes) > 0, f"No workflow routes found. Routes: {routes}"

def test_health_check():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
