import pytest
from maas_document_system.agents.reviewer_agent import ReviewerAgent
from agno.models.anthropic import Claude

def test_reviewer_agent_initialization():
    agent = ReviewerAgent()
    assert isinstance(agent.model, Claude)
    assert agent.model.id == "claude-3-7-sonnet-latest"
