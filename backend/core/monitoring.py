import os
import agentops
from backend.core.config import settings
from backend.core.logging import logger

def init_monitoring():
    """
    Initialize AgentOps for multi-agent observability.
    """
    if settings.AGENTOPS_API_KEY and settings.ENABLE_TELEMETRY:
        try:
            agentops.init(api_key=settings.AGENTOPS_API_KEY)
            logger.info("AgentOps initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize AgentOps: {e}")
    else:
        logger.info("AgentOps monitoring is disabled or API key is missing.")

def track_agent(agent_name: str):
    """
    Decorator or helper to track specific agent activities if needed.
    AgentOps often handles this automatically via SDK integration with LLMs.
    """
    return agentops.track_agent(name=agent_name)
