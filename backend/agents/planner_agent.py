from agno.agent import Agent
from backend.agents.base import get_model
from backend.schemas.models import DocumentPlan, ProjectMetadata
from backend.tools.integrations.redmine_tools import RedmineTools
from backend.tools.local.enterprise_tools import EnterpriseTools
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class PlannerAgent(Agent):
    """
    PlannerAgent is responsible for creating a structured document plan
    based on project metadata and live Redmine data.
    """
    
    def __init__(self):
        llm = get_model()
        super().__init__(
            model=llm,
            description="You are a Senior Document Planner for AgentOS.",
            instructions=[
                "Analyze the project metadata to understand the scope and type of the document.",
                "If a project identifier/ID is available, ALWAYS use `get_project_context` from Redmine.",
                "Use `EnterpriseTools` (get_project_viability) to get the latest financial status.",
                "Structure the document into logical sections (e.g., Executive Summary, Method, Results).",
                "Ensure the output conforms exactly to the DocumentPlan schema."
            ],
            tools=[RedmineTools(), EnterpriseTools()],
            markdown=True,
            output_schema=DocumentPlan
        )

    def create_plan(self, job_id: str, metadata: ProjectMetadata) -> DocumentPlan:
        """
        Generates a document plan.
        """
        logger.info(f"PlannerAgent: Creating plan for Job {job_id}")
        
        prompt = f"""
        Create a comprehensive Document Plan for:
        Project: {metadata.project_name}
        Client: {metadata.client_name}
        Type: {metadata.project_type}
        Description: {metadata.description}
        
        If 'template_name' was '{metadata.template_name}', ensure the structure aligns with it if possible.
        """
        
        try:
            response = self.run(prompt)
            if response and response.content:
                plan = response.content
                if isinstance(plan, DocumentPlan):
                    plan.project_id = job_id
                    return plan
        except Exception as e:
            logger.error(f"PlannerAgent failed: {e}")
            
        # Fallback
        return DocumentPlan(project_id=job_id, title=metadata.project_name, sections=[])
