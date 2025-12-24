from agno.agent import Agent
from backend.agents.base import get_model
from typing import List, Dict

class ContextBrokerAgent(Agent):
    """
    ContextBrokerAgent uses Hybrid Search (RAG) to find and prune context,
    providing only the most relevant evidence for a specific subsection.
    """
    def __init__(self):
        llm = get_model()
        super().__init__(
            model=llm,
            description="You are a Context Optimization Specialist.",
            instructions=[
                "Analyze the subsection objectives.",
                "Search the Knowledge base and Redmine evidence.",
                "Select and summarize only the top 3 most relevant pieces of evidence.",
                "Minimize the token footprint for the AuthorAgent."
            ]
        )

    def get_pruned_context(self, objectives: List[str], project_data: Dict) -> str:
        """
        Mock of a hybrid search and context pruning operation.
        """
        # In production, this would use VectorDB Hybrid Search
        relevant_context = f"Found relevant evidence for {objectives[0]}: \n- Data Point A\n- Data Point B"
        return relevant_context
