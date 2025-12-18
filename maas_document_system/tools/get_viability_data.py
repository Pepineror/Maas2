from agno.tools import Toolkit
from maas_document_system.schemas.tool_outputs import ViabilityMetrics

class ViabilityTools(Toolkit):
    def __init__(self):
        super().__init__(name="viability_tools")
        self.register(self.get_project_viability)

    def get_project_viability(self, project_name: str) -> ViabilityMetrics:
        """
        Retrieves viability metrics for a given project name.
        Mocks data based on deterministic hashing of the name for dry-run consistency.
        
        Args:
            project_name (str): The name of the project.

        Returns:
            ViabilityMetrics: Structured viability data.
        """
        # Deterministic mock logic
        hash_val = hash(project_name)
        score = abs(hash_val % 100)
        roi = abs(hash_val % 200) / 10.0
        
        risk = "Low"
        if score < 50:
            risk = "High"
        elif score < 75:
            risk = "Medium"
            
        return ViabilityMetrics(
            project_name=project_name,
            roi_estimate=roi,
            viability_score=score,
            risk_level=risk,
            details={"mock_source": "internal_db_stub"}
        )
