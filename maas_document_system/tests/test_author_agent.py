import pytest
from maas_document_system.agents.author_agent import AuthorAgent
from agno.models.openai import OpenAIChat

def test_author_agent_initialization():
    agent = AuthorAgent()
    assert isinstance(agent.model, OpenAIChat)
    assert agent.model.id == "gpt-4o"
    assert len(agent.tools) >= 2
