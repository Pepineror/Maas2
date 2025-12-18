import pytest
from pydantic import ValidationError
from maas_document_system.schemas.project_metadata import ProjectMetadata
from maas_document_system.schemas.audit_log import AuditLog, AuditAction
from maas_document_system.schemas.section_content import SectionContent, SectionStatus
from maas_document_system.schemas.document_plan import DocumentPlan, PlanItem
from maas_document_system.schemas.final_document import FinalDocument

# --- ProjectMetadata Tests ---
def test_project_metadata_valid():
    data = {
        "project_name": "Test Project",
        "client_name": "Test Client",
        "project_type": "report"
    }
    model = ProjectMetadata(**data)
    assert model.project_name == "Test Project"
    assert model.priority == "normal"  # Default value

def test_project_metadata_invalid():
    with pytest.raises(ValidationError):
        ProjectMetadata(project_name="TP", client_name="X", project_type="Y") # Too short

def test_extra_fields_forbidden():
    with pytest.raises(ValidationError):
        ProjectMetadata(
            project_name="OK", 
            client_name="Client", 
            project_type="Report", 
            extra_field="Should Fail"
        )

# --- AuditLog Tests ---
def test_audit_log_creation():
    log = AuditLog(
        job_id="job-1",
        actor="TestBot",
        action=AuditAction.CREATED,
        target="Section-X",
        result="Success"
    )
    assert log.job_id == "job-1"

def test_audit_log_immutability():
    log = AuditLog(
        job_id="job-1",
        actor="TestBot",
        action=AuditAction.CREATED,
        target="Section-X",
        result="Success"
    )
    with pytest.raises(ValidationError):
        log.result = "Changed" # Should fail due to frozen=True

# --- SectionContent Tests ---
def test_section_content_valid():
    section = SectionContent(
        plan_id="plan-1",
        title="Intro",
        content_md="# Head"
    )
    assert section.status == SectionStatus.PLANNED
    assert section.hierarchy_level == 1

# --- DocumentPlan Tests ---
def test_document_plan_valid():
    item = PlanItem(
        section_id="sec-1",
        title="Intro",
        description_prompt="Write intro",
        hierarchy_level=1,
        order_index=0
    )
    plan = DocumentPlan(
        job_id="job-1",
        outline=[item]
    )
    assert len(plan.outline) == 1
    assert plan.outline[0].title == "Intro"

# --- FinalDocument Tests ---
def test_final_document_valid():
    final = FinalDocument(
        job_id="job-1",
        total_sections=10
    )
    assert final.job_id == "job-1"
