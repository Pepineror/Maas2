from agno.agent import Agent
from .base import get_model
from maas_document_system.schemas.section_content import SectionContent, SectionStatus
from maas_document_system.schemas.document_plan import PlanItem
from maas_document_system.tools.get_viability_data import ViabilityTools
from maas_document_system.tools.fetch_source_text import SourceTextTools
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class AuthorAgent(Agent):
    """
    AuthorAgent writes high-quality section content using available tools.
    
    Model: GPT-4o
    Tools: ViabilityTools, SourceTextTools
    """
    
    def __init__(self):
        llm = get_model()
        super().__init__(
            model=llm,
            description="You are an expert Content Author for technical documents.",
            instructions=[
                "Analyze the section title and prompt provided.",
                "Use `ViabilityTools` to fetch data if the section relates to viability/metrics.",
                "Use `SourceTextTools` if you need to fetch content from external URLs.",
                "Write clear, professional, and well-structured markdown content.",
                "Output must strictly follow the SectionContent schema."
            ],
            tools=[ViabilityTools(), SourceTextTools()],
            markdown=True,

        )

    def write_section(self, plan_item: PlanItem, plan_id: str) -> SectionContent:
        """
        Generates content for a section.
        """
        logger.info(f"AuthorAgent: Writing section '{plan_item.title}'")
        
        prompt = f"""
        Write content for the following section:
        Title: {plan_item.title}
        Context/Instructions: {plan_item.description_prompt}
        
        Ensure the content is detailed and addresses the instructions.
        """
        
        try:
            response = self.run(prompt)
            if response and response.content:
                content_obj = response.content
                if isinstance(content_obj, SectionContent):
                    content_obj.plan_id = plan_id
                    content_obj.title = plan_item.title
                    content_obj.hierarchy_level = plan_item.hierarchy_level
                    content_obj.status = SectionStatus.DRAFTED
                    return content_obj
        except Exception as e:
            logger.error(f"AuthorAgent failed: {e}")

        # Fallback
        return SectionContent(
            plan_id=plan_id,
            title=plan_item.title,
            hierarchy_level=plan_item.hierarchy_level,
            content_md=f"## {plan_item.title}\n\n[Error generating content]",
            status=SectionStatus.FAILED
        )
