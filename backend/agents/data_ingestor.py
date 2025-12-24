from agno.agent import Agent
from backend.core.redis_client import redis_client
from backend.core.logging import logger
from backend.schemas.models import ProjectMetadata
import time

class DataIngestor(Agent):
    """
    DataIngestor performs asynchronous ETL to extract project viability data
    from legacy systems and populate the RealTimeCache.
    """
    def __init__(self):
        super().__init__(
            name="data_ingestor",
            description="ETL Agent for project data ingestion.",
            instructions=[
                "Extract financial metrics from SAP and progression from P6 (Mocked).",
                "Normalize data into the standard ViabilityMetrics schema.",
                "Populate the Redis cache for immediate availability."
            ]
        )

    def ingest_project_data(self, project_id: str, metadata: ProjectMetadata):
        """
        Simulates an ETL run for a specific project.
        """
        logger.info(f"DataIngestor: Starting ingestion for project {project_id}")
        
        # Mocking an ETL process
        mock_data = {
            "project_name": metadata.project_name,
            "roi_estimate": 15.5,
            "viability_score": 88,
            "risk_level": "Low",
            "extracted_at": time.time(),
            "source": "SAP/P6 Integration"
        }
        
        # Cache for 24 hours
        redis_client.set(f"viability:{project_id}", mock_data, expire_seconds=86400)
        logger.info(f"DataIngestor: Cache populated for {project_id}")
        return mock_data
