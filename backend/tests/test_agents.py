import pytest
import os
from backend.agents.planner_agent import PlannerAgent
from backend.agents.author_agent import AuthorAgent
from backend.agents.reviewer_agent import ReviewerAgent
from backend.schemas.models import ProjectMetadata, ProjectType, DocumentPlan, DocumentSection, ReviewResult
from backend.schemas.tool_outputs import SectionContent

@pytest.fixture
def planner():
    return PlannerAgent()

@pytest.fixture
def author():
    return AuthorAgent()

@pytest.fixture
def reviewer():
    return ReviewerAgent()

def test_planner_initialization(planner):
    assert planner.output_schema == DocumentPlan

def test_author_initialization(author):
    assert author.output_schema == SectionContent

def test_reviewer_initialization(reviewer):
    assert reviewer.output_schema == ReviewResult

def test_planner_create_plan_mock(planner, monkeypatch):
    metadata = ProjectMetadata(
        project_name="Test Project",
        client_name="Test Client",
        description="Test plan"
    )
    # Mock the internal run call to avoid real LLM
    from agno.models.response import ModelResponse
    monkeypatch.setattr(planner, "run", lambda p: ModelResponse(
        content=DocumentPlan(project_id="test-123", title="Test Plan", sections=[])
    ))
    
    plan = planner.create_plan(job_id="test-123", metadata=metadata)
    assert plan.project_id == "test-123"
    assert plan.title == "Test Plan"

def test_author_write_section_mock(author, monkeypatch):
    section = DocumentSection(title="S1", content="Instruction")
    from agno.models.response import ModelResponse
    monkeypatch.setattr(author, "run", lambda p: ModelResponse(
        content=SectionContent(project_id="test-123", title="S1", content_md="# S1 content")
    ))
    
    draft = author.write_section(project_id="test-123", section=section)
    assert draft.title == "S1"
    assert "# S1 content" in draft.content_md
