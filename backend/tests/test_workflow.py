import pytest
import os
import shutil
from backend.workflows.document_creation_workflow import DocumentCreationWorkflow
from backend.schemas.models import ProjectMetadata, FinalDocument

@pytest.fixture
def workflow():
    return DocumentCreationWorkflow()

def test_workflow_initialization(workflow):
    assert workflow.name == "autonomous_document_workflow"
    assert workflow.planner is not None
    assert workflow.author is not None

def test_workflow_run_mock(workflow, monkeypatch):
    """
    Test a dry run of the workflow with mocked agent calls.
    """
    metadata = ProjectMetadata(
        project_name="Autonomous Test Project",
        client_name="Test Client",
        description="Testing the v4.0 workflow"
    )
    
    # Mocking the internal methods of agents or the workflow steps
    # to avoid real LLM calls and Redis dependencies
    
    # Mocking DataIngestor
    monkeypatch.setattr(workflow.data_ingestor, "ingest_project_data", lambda pid, meta: {"data": "mock"})
    
    # Mocking Extractor
    from backend.schemas.tool_outputs import ViabilityMetrics
    monkeypatch.setattr(workflow.extractor, "get_viability", lambda pid: ViabilityMetrics(
        project_name="Mock", roi_estimate=0.85, viability_score=90, risk_level="Low"
    ))
    
    # Mocking Planner
    from backend.schemas.models import DocumentPlan, DocumentSection
    monkeypatch.setattr(workflow.planner, "create_plan", lambda job_id, metadata: DocumentPlan(
        project_id=job_id,
        title="Mock Plan",
        sections=[DocumentSection(title="S1", content="C1")]
    ))
    
    # Mocking Author (via write_section_async or author.write_section)
    from backend.schemas.tool_outputs import SectionContent
    monkeypatch.setattr(workflow.author, "write_section", lambda project_id, section: SectionContent(
        project_id=project_id, title=section.title, content_md="# Section 1\nGenerated content"
    ))

    # Mocking MicroPlanner
    from backend.schemas.models import SectionDecomposition
    monkeypatch.setattr(workflow.micro_planner, "decompose_section", lambda section: SectionDecomposition(
        section_title=section.title, subsections=[]
    ))
    
    # Mocking ContextBroker
    monkeypatch.setattr(workflow.context_broker, "get_pruned_context", lambda q, ctx: "Mocked pruned context")

    # Mocking delivery agents
    monkeypatch.setattr(workflow.notifier, "notify", lambda msg, level="info": None)
    monkeypatch.setattr(workflow.validator, "validate", lambda t, c, context: True)

    final_doc = workflow.run(input=metadata, run_id="test-run-123")
    
    assert isinstance(final_doc, FinalDocument)
    assert final_doc.project_id == "test-run-123"
    assert "Generated content" in final_doc.full_text
    assert os.path.exists(final_doc.file_path)
    
    # Cleanup
    if os.path.exists(os.path.dirname(final_doc.file_path)):
        shutil.rmtree(os.path.dirname(final_doc.file_path))
