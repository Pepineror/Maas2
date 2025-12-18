import pytest
from maas_document_system.agents.planner_agent import PlannerAgent
from agno.models.anthropic import Claude

def test_planner_agent_initialization():
    agent = PlannerAgent()
    assert isinstance(agent.model, Claude)
    assert agent.model.id == "claude-3-7-sonnet-latest"
    assert len(agent.tools) > 0 # Should have RedmineTools
