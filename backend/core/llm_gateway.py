from typing import Optional
from agno.models.openai import OpenAIChat
from backend.core.config import settings
from backend.core.logging import logger

class LLMGateway:
    """
    LLMGateway handles Tiered Model Routing and Streaming.
    Tiers:
    - Tier 1: Fast/Cheap (GPT-4o-mini / Flash models) - Planning, ETL summaries.
    - Tier 2: Quality/Reasoning (GPT-4o / Claude 3.7) - Provision, Technical Prose.
    - Tier 3: Reasoning Deep (o1 / o3-mini) - Complex architectural validation.
    """
    
    @staticmethod
    def get_model(tier: int = 2, streaming: bool = False):
        """
        Returns a model instance based on the requested tier.
        """
        # Mapping tiers to models (using OpenAI as primary for MVP)
        if tier == 1:
            model_id = "gpt-4o-mini"
        elif tier == 3:
            model_id = "o3-mini" # Or o1-preview
        else:
            model_id = "gpt-4o"

        logger.info(f"LLMGateway: Routing to {model_id} (Tier {tier}, Streaming: {streaming})")
        
        return OpenAIChat(
            id=model_id,
            api_key=settings.OPENAI_API_KEY or "none"
        )

# Export a convenience function similar to the old base.py but with tier support
def get_model(tier: int = 2, streaming: bool = False):
    return LLMGateway.get_model(tier=tier, streaming=streaming)
