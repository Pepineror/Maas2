from fastapi.testclient import TestClient
from maas_document_system.app.serve import app
import pytest

client = TestClient(app)

def test_submit_job():
    payload = {
        "prompt": "Create a viability study for a new park",
        "project_name": "New Park Project",
        "user_id": "test-user"
    }
    response = client.post("/openwebui/jobs", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "queued"
    
def test_get_job_status_not_found():
    response = client.get("/openwebui/jobs/missing-job-id")
    assert response.status_code == 404

# Note: Testing the full background task execution requires mocking the workflow or allowing it to run.
# Since we use in-memory store, we might be able to intercept if we mock the workflow run.
