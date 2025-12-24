from agno.agent import Agent
from backend.agents.base import get_model
from backend.schemas.models import DocumentSection
from pydantic import BaseModel, Field
from typing import List

class SubsectionPlan(BaseModel):
    title: str
    objectives: List[str]
    context_tags: List[str]

class SectionDecomposition(BaseModel):
    subsections: List[SubsectionPlan]

class MicroPlannerAgent(Agent):
    """
    MicroPlannerAgent decomposes a complex document section into atomic subsections
    based on the document templates.
    """
    def __init__(self):
        llm = get_model()
        super().__init__(
            model=llm,
            description="You are a Micro-Planning Specialist for document structure.",
            instructions=[
                "Break down the provided section into 3-5 logical subsections.",
                "For each subsection, define clear writing objectives and context requirements.",
                "Ensure the structure supports parallel generation (Map-Reduce)."
            ],
            output_schema=SectionDecomposition
        )

    def decompose_section(self, section: DocumentSection) -> SectionDecomposition:
        """
        Decomposes a section into subsections.
        """
        prompt = f"Decompose the following section into a micro-plan: {section.title}\nDescription: {section.content}"
        response = self.run(prompt)
        if response and response.content:
            return response.content
        return SectionDecomposition(subsections=[])
