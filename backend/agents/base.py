import logging
import os
from agno.models.base import Model
from backend.core.config import settings

logger = logging.getLogger(__name__)

from backend.core.llm_gateway import LLMGateway

def get_model(tier: int = 2, streaming: bool = False):
    """Factory to return the configured LLM model via LLMGateway."""
    return LLMGateway.get_model(tier=tier, streaming=streaming)
