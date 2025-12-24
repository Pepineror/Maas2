from agno.tools import Toolkit
from backend.core.redis_client import redis_client
from backend.schemas.tool_outputs import ViabilityMetrics, SourceContent
import hashlib

class EnterpriseTools(Toolkit):
    """
    Tools for the Enterprise MAAS v4.0 Tool Server.
    Exposes project viability and evidence retrieval to the agents.
    """
    def __init__(self):
        super().__init__(name="enterprise_tools")
        self.register(self.get_project_viability)
        self.register(self.get_evidence_snippet)

    def get_project_viability(self, project_id: str) -> ViabilityMetrics:
        """
        Retrieves in-real time risk scores and metrics from the RealTimeCache.
        """
        cached = redis_client.get(f"viability:{project_id}")
        if cached:
            return ViabilityMetrics(**cached)
        return ViabilityMetrics(
            project_name="Pending", 
            roi_estimate=0.0, 
            viability_score=0, 
            risk_level="Unknown", 
            details={"status": "data_not_ready"}
        )

    def get_evidence_snippet(self, source_id: str) -> SourceContent:
        """
        Recovers the exact text snippet from the EvidenceMetadata Vector Store.
        """
        # Mocking a VectorDB retrieval
        content = f"Official evidence for {source_id}: Strategic alignment confirmed with Codelco 2030 vision."
        return SourceContent(
            source_id=source_id,
            content_text=content,
            sha256_hash=hashlib.sha256(content.encode()).hexdigest(),
            metadata={"source": "vector_db_stub"}
        )

# Tool server instance
enterprise_tools = EnterpriseTools()
