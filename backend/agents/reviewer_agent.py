from agno.agent import Agent
from backend.agents.base import get_model
from backend.schemas.models import ReviewResult
import logging

logger = logging.getLogger(__name__)

class ReviewerAgent(Agent):
    """
    ReviewerAgent checks content quality, tone, and accuracy.
    """
    
    def __init__(self):
        llm = get_model()
        super().__init__(
            model=llm,
            description="You are a meticulous Senior Editor and Reviewer.",
            instructions=[
                "Review the provided content for clarity, grammar, tone, and logical flow.",
                "Check if the content adheres to the section title and instructions provided.",
                "Provide constructive feedback if improvements are needed.",
                "Assign a quality score from 1 to 10.",
                "Return a ReviewResult object."
            ],
            markdown=True,
            output_schema=ReviewResult
        )

    def review_content(self, title: str, content: str, instructions: str) -> ReviewResult:
        """
        Reviews a section's content.
        """
        prompt = f"""
        Review the following section:
        
        Title: {title}
        Contextual instructions: {instructions}
        
        Content to review:
        {content}
        """
        
        try:
            response = self.run(prompt)
            if response and response.content:
                return response.content
        except Exception as e:
            logger.error(f"ReviewerAgent failed: {e}")
            
        return ReviewResult(is_approved=False, feedback="Review failed due to error.", score=0)
