from agno.agent import Agent
from backend.core.redis_client import redis_client
from backend.schemas.tool_outputs import ViabilityMetrics
from backend.core.logging import logger

class ExtractorAgent(Agent):
    """
    ExtractorAgent retrieves project data using a Cache-First strategy.
    """
    def __init__(self):
        super().__init__(
            name="extractor_agent",
            description="Agent for retrieving evidence and metrics with extreme low latency.",
            instructions=[
                "Always check the RealTimeCache (Redis) first.",
                "If data is missing, notify the system to trigger a fresh ETL run.",
                "Provide structured evidence to the AuthorAgent."
            ]
        )

    def get_viability(self, project_id: str) -> ViabilityMetrics:
        """
        Retrieves viability metrics from cache.
        """
        cached_data = redis_client.get(f"viability:{project_id}")
        if cached_data:
            logger.info(f"ExtractorAgent: Cache hit for {project_id}")
            return ViabilityMetrics(**cached_data)
        
        logger.warning(f"ExtractorAgent: Cache miss for {project_id}")
        # In a full DAG, this would trigger a sub-workflow or wait for DataIngestor
        return ViabilityMetrics(
            project_name="Unknown", 
            roi_estimate=0.0, 
            viability_score=0, 
            risk_level="High", 
            details={"error": "data_not_in_cache"}
        )
