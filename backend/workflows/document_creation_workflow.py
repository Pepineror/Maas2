import os
import asyncio
from typing import List, Optional, Any
from datetime import datetime
from agno.workflow import Workflow
from agno.utils.log import logger

from backend.schemas.models import ProjectMetadata, FinalDocument, DocumentSection
from backend.schemas.tool_outputs import SectionContent
from backend.agents.planner_agent import PlannerAgent
from backend.agents.author_agent import AuthorAgent
from backend.agents.data_ingestor import DataIngestor
from backend.agents.extractor_agent import ExtractorAgent
from backend.agents.micro_planner import MicroPlannerAgent
from backend.agents.context_broker import ContextBrokerAgent
from backend.agents.delivery_agents import IntegratorAgent, NotifierAgent, ValidatorAgent
from backend.agents.persist_agent import persist_agent
from backend.knowledge.template_manager import template_manager
from backend.core.config import settings
from backend.agents.base import get_model

class DocumentCreationWorkflow(Workflow):
    """
    Autonomous Enterprise MAAS Workflow (v4.0).
    Orchestrates: ETL -> Plan -> Micro-Plan -> Parallel Draft -> Optimistic Delivery -> Async Validation.
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="autonomous_document_workflow",
            description="Autonomous DAG for SIC/API document generation.",
            input_schema=ProjectMetadata,
            **kwargs
        )
        
        # 1. Planning & Extraction (Tier 1)
        self.planner = PlannerAgent() 
        self.data_ingestor = DataIngestor()
        self.extractor = ExtractorAgent()
        
        # 2. Drafting (Tier 2/Streaming)
        self.author = AuthorAgent() # AuthorAgent's internal __init__ uses base.get_model()
        self.micro_planner = MicroPlannerAgent()
        self.context_broker = ContextBrokerAgent()
        
        # 3. Delivery & Validation (Tier 3)
        self.integrator = IntegratorAgent()
        self.notifier = NotifierAgent()
        self.validator = ValidatorAgent()
        self.persist = persist_agent

    async def write_section_async(self, project_id: str, section: DocumentSection, project_data: Any) -> SectionContent:
        """
        Sub-flow for a single section: Micro-Plan -> Context Pruning -> Draft.
        """
        try:
            self.notifier.notify(f"Micro-planning section: {section.title}")
            micro_plan = self.micro_planner.decompose_section(section)
            
            # Combine pruned context for all subsections
            full_pruned_context = ""
            for sub in micro_plan.subsections:
                pruned = self.context_broker.get_pruned_context(sub.objectives, project_data)
                full_pruned_context += f"\n### {sub.title}\n{pruned}"
            
            # Update section instruction with pruned context
            section.content = f"{section.content or ''}\n\nRELEVANT EVIDENCE:\n{full_pruned_context}"
            
            # Draft section
            draft = self.author.write_section(project_id=project_id, section=section)
            
            # Commit Fragment (Tri-layer)
            self.persist.commit_fragment(
                project_id=project_id, 
                section_title=section.title, 
                content=draft.content_md,
                metadata={"status": draft.status}
            )
            return draft
        except Exception as e:
            logger.error(f"Failed to process section {section.title}: {e}")
            return SectionContent(project_id=project_id, title=section.title, content_md="Error", status="failed")

    def run(self, input: ProjectMetadata, run_id: Optional[str] = None, **kwargs) -> FinalDocument:
        """
        Executes the full DAG synchronously (using an internal event loop for parallel tasks).
        """
        project_id = run_id or f"autodoc-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        self.notifier.notify(f"Starting Autonomous Workflow v4.0 for {input.project_name}", level="info")
        
        # 1. Data Ingestion (ETL) & Extraction
        self.notifier.notify("Etapa 2: Ingesta de datos y búsqueda de viabilidad...")
        project_data = self.data_ingestor.ingest_project_data(project_id, input)
        viability = self.extractor.get_viability(project_id)
        
        # Update metadata with viability info for the Planner
        input.description = f"VIABILITY DATA: {viability.model_dump_json()}\n---\n{input.description}"

        # 2. Macro-Planning
        self.notifier.notify("Etapa 3: Planificación macro por contrato...")
        if input.template_name:
            template_content = template_manager.get_template(input.template_name)
            if template_content:
                input.description = f"TEMPLATE CONTEXT:\n{template_content}\n---\n{input.description}"

        document_plan = self.planner.create_plan(job_id=project_id, metadata=input)
        
        # 3. Parallel Execution (Map-Reduce)
        self.notifier.notify(f"Etapa 4: Generación paralela de {len(document_plan.sections)} secciones...")
        
        # Since 'run' is sync, we use loop.run_until_complete for the parallel part
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        tasks = [self.write_section_async(project_id, sec, project_data) for sec in document_plan.sections]
        results: List[SectionContent] = loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()

        # 4. Optimistic Delivery & Integration
        self.notifier.notify("Etapa 5: Consolidación y entrega optimista...")
        fragments = [r.content_md for r in results]
        full_text = self.integrator.assemble(fragments)
        
        file_path = self.persist.finalize_document(project_id, full_text)
            
        final_doc = FinalDocument(
            project_id=project_id,
            title=document_plan.title,
            full_text=full_text,
            file_path=file_path,
            metadata={"status": "optimistic_delivery", "viability_score": viability.viability_score}
        )

        # 5. Background Validation
        for r in results:
            self.validator.validate(r.title, r.content_md, context=str(project_data))
        
        self.notifier.notify("Workflow completado. Documento disponible para revisión.")
        return final_doc
