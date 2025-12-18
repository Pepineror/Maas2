from agno.agent import Agent
from .base import get_model
from maas_document_system.schemas.document_plan import DocumentPlan, PlanItem
from maas_document_system.schemas.project_metadata import ProjectMetadata
from maas_document_system.tools.redmine_tools import RedmineTools
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class PlannerAgent(Agent):
    """
    PlannerAgent is responsible for creating a structured document plan
    based on project metadata and live Redmine data.
    
    Model: Claude 3.7 Sonnet (Reasoning)
    Tools: RedmineTools
    """
    
    def __init__(self):
        llm = get_model()
        super().__init__(
            model=llm,
            description="You are a Senior Document Planner for AgentOS.",
            instructions=[
                "Analyze the project metadata to understand the scope and type of the document.",
                "If a project identifier/ID is available, ALWAYS use `get_project_context` to fetch live data from Redmine.",
                "Structure the document into logical sections (e.g., Executive Summary, Method, Results).",
                "For each section, provide a detailed `description_prompt` that guides the AuthorAgent.",
                "Ensure the output conforms exactly to the DocumentPlan schema."
            ],
            tools=[RedmineTools()],
            markdown=True,

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
        
        If 'template_name' was '{metadata.template_name}', ensure the structure aligns with it if possible, 
        or define a standard structure for this project type.
        """
        
        try:
            response = self.run(prompt)
            # Agno returns RunResponse, .content is the model object if output_model is set
            if response and response.content:
                plan = response.content
                if isinstance(plan, DocumentPlan):
                    plan.job_id = job_id
                    return plan
        except Exception as e:
            logger.error(f"PlannerAgent failed: {e}")
            
        # Fallback
        return DocumentPlan(job_id=job_id, outline=[])
