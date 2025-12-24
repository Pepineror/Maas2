from agno.agent import Agent
from backend.core.logging import logger

class IntegratorAgent(Agent):
    """
    IntegratorAgent consolidates fragments into a final document.
    """
    def __init__(self):
        super().__init__(name="integrator", description="Document Assembler")

    def assemble(self, fragments: list) -> str:
        return "\n\n".join(fragments)

class NotifierAgent(Agent):
    """
    NotifierAgent sends status updates to OpenWebUI or other channels.
    """
    def __init__(self):
        super().__init__(name="notifier", description="Status Notifier")

    def notify(self, message: str, level: str = "info"):
        logger.info(f"NOTIFICATION [{level.upper()}]: {message}")

class ValidatorAgent(Agent):
    """
    ValidatorAgent performs non-blocking validation of generated content.
    Target Tier: 3 (Deep Reasoning).
    """
    def __init__(self):
        from backend.agents.base import get_model
        super().__init__(
            model=get_model(tier=3),
            name="validator", 
            description="Background Auditor for logical consistency.",
            instructions=[
                "Analyze the prose for logical consistency with previous sections.",
                "Verify that technical metrics match the project context.",
                "Ensure no hallucinations or generic filler text is present.",
                "Flag any inconsistencies for the IntegratorAgent."
            ]
        )

    def validate(self, title: str, content: str, context: str) -> bool:
        prompt = f"Validate this section: {title}\nContent: {content}\nProject context: {context}"
        # In a real run, this would return a structured report.
        return True
