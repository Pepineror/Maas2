from agno.agent import Agent
from backend.agents.base import get_model
from backend.schemas.tool_outputs import SectionContent
from backend.schemas.models import DocumentSection
from backend.tools.local.viability_tools import ViabilityTools
from backend.tools.local.source_text_tools import SourceTextTools
from backend.tools.local.enterprise_tools import EnterpriseTools
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class AuthorAgent(Agent):
    """
    AuthorAgent writes high-quality section content using available tools.
    """
    
    def __init__(self):
        llm = get_model()
        super().__init__(
            model=llm,
            description="You are an expert Content Author for technical documents.",
            instructions=[
                "Analyze the section title and description provided by the Planner.",
                "Use `EnterpriseTools` (get_project_viability) ALWAYS for metrics and calculations.",
                "Use `EnterpriseTools` (get_evidence_snippet) for RAG evidence.",
                "Use `ViabilityTools` and `SourceTextTools` as fallback.",
                "Write clear, professional markdown content."
            ],
            tools=[EnterpriseTools(), ViabilityTools(), SourceTextTools()],
            markdown=True,
            output_schema=SectionContent
        )

    def write_section(self, project_id: str, section: DocumentSection) -> SectionContent:
        """
        Generates content for a document section.
        """
        logger.info(f"AuthorAgent: Writing section '{section.title}'")
        
        prompt = f"""
        Project ID: {project_id}
        Section Title: {section.title}
        Description/Instructions: {section.content or 'Write a detailed section based on the title.'}
        
        Provide professional content in markdown.
        """
        
        try:
            response = self.run(prompt)
            if response and response.content:
                content_obj = response.content
                if isinstance(content_obj, SectionContent):
                    content_obj.project_id = project_id
                    content_obj.title = section.title
                    return content_obj
        except Exception as e:
            logger.error(f"AuthorAgent failed: {e}")

        # Fallback
        return SectionContent(
            project_id=project_id,
            title=section.title,
            content_md=f"## {section.title}\n\n[Error generating content for this section]",
            status="failed"
        )
