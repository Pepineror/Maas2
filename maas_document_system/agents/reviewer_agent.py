from agno.agent import Agent
from .base import get_model
from pydantic import BaseModel, Field
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class ReviewResult(BaseModel):
    """
    Schema for the output of a review.
    """
    is_approved: bool = Field(..., description="Whether the content is approved.")
    feedback: str = Field(..., description="Detailed feedback or suggested improvements.")
    score: int = Field(..., description="Quality score from 1-10.")

class ReviewerAgent(Agent):
    """
    ReviewerAgent checks content quality, tone, and accuracy.
    
    Model: Claude 3.7 Sonnet (Reasoning)
    """
    
    def __init__(self):
        llm = get_model()
        super().__init__(
            model=llm,
            description="You are a meticulous Senior Editor and Reviewer.",
            instructions=[
                "Review the provided content for clarity, grammar, tone, and logical flow.",
                "Check if the content adheres to the section title and prompt instructions.",
                "Provide constructive feedback if changes are needed.",
                "Assign a quality score from 1 to 10.",
                "Return a ReviewResult object."
            ],
            markdown=True
        )

    def review_content(self, title: str, content: str, instructions: str) -> ReviewResult:
        """
        Reviews a section's content.
        """
        prompt = f"""
        Review the following section:
        
        Title: {title}
        Instructions given to author: {instructions}
        
        Content:
        {content}
        """
        
        try:
            response = self.run(prompt)
            if response and response.content:
                return response.content
        except Exception as e:
            logger.error(f"ReviewerAgent failed: {e}")
            
        return ReviewResult(is_approved=False, feedback="Review failed due to error.", score=0)
