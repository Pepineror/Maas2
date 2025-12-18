import pytest
import os
from maas_document_system.agents.planner_agent import PlannerAgent
from maas_document_system.agents.author_agent import AuthorAgent
from maas_document_system.agents.reviewer_agent import ReviewerAgent
from maas_document_system.schemas.project_metadata import ProjectMetadata, ProjectType
from maas_document_system.schemas.document_plan import DocumentPlan, PlanItem
from maas_document_system.schemas.section_content import SectionContent, SectionStatus

# Using MockModel approach since no API_KEY present in this environment by default
@pytest.fixture(autouse=True)
def ensure_no_api_key():
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

def test_planner_agent_dry_run():
    planner = PlannerAgent()
    metadata = ProjectMetadata(
        project_name="Test Project",
        client_name="Test Client",
        project_type=ProjectType.RESEARCH_REPORT,
        description="A test project"
    )
    
    plan = planner.create_plan(job_id="job-123", metadata=metadata)
    
    assert isinstance(plan, DocumentPlan)
    assert plan.job_id == "job-123"
    # Basic check that we got a valid mock plan back
    assert len(plan.outline) > 0

def test_author_agent_dry_run():
    author = AuthorAgent()
    plan_item = PlanItem(
        section_id="sec-1",
        title="Introduction", 
        description_prompt="Write intro",
        hierarchy_level=1,
        order_index=0
    )
    
    section = author.write_section(plan_item, plan_id="plan-123")
    
    assert isinstance(section, SectionContent)
    assert section.title == "Introduction"
    assert "Generated content" in section.content_md

def test_reviewer_agent_dry_run():
    reviewer = ReviewerAgent()
    section = SectionContent(
        plan_id="plan-123",
        title="Intro",
        hierarchy_level=1,
        content_md="Some content",
        status=SectionStatus.DRAFTED
    )
    
    result = reviewer.review_section(section)
    
    assert result.approved is True
    assert result.quality_score > 0
