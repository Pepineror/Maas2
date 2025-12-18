import pytest
import os
from maas_document_system.workflows.document_creation_workflow import DocumentCreationWorkflow
from maas_document_system.schemas.project_metadata import ProjectMetadata, ProjectType
from maas_document_system.schemas.final_document import FinalDocument

# Using MockModel approach since no API_KEY present
@pytest.fixture(autouse=True)
def ensure_no_api_key():
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

def test_workflow_end2end_dry_run():
    # Job ID is now handled internally or via run_id.
    workflow = DocumentCreationWorkflow()
    
    metadata = ProjectMetadata(
        project_name="End-to-End Test Project",
        client_name="Test Client",
        project_type=ProjectType.RESEARCH_REPORT,
        description="Testing the full workflow"
    )
    
    # We can pass run_id if we want to control it, or let it generate.
    # For test assert, we might want to capture it or assume auto-generation works.
    final_doc = workflow.run(input=metadata)
    
    assert isinstance(final_doc, FinalDocument)
    # assert final_doc.job_id == "wf-job-123" # No longer fixed, unless we mock run_id
    assert final_doc.job_id.startswith("job-") or final_doc.job_id == "mock-run-id"
    assert final_doc.markdown_path is not None
    assert os.path.exists(final_doc.markdown_path)
    
    with open(final_doc.markdown_path, "r") as f:
        content = f.read()
        assert "End-to-End Test Project" in content
        assert "Generated content" in content
