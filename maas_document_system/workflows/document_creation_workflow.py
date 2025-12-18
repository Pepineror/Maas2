from typing import List, Optional, Any
from agno.workflow import Workflow
from agno.utils.log import logger
from maas_document_system.schemas.project_metadata import ProjectMetadata
from maas_document_system.schemas.document_plan import DocumentPlan
from maas_document_system.schemas.section_content import SectionContent, SectionStatus
from maas_document_system.schemas.final_document import FinalDocument
from maas_document_system.agents.planner_agent import PlannerAgent
from maas_document_system.agents.author_agent import AuthorAgent
from maas_document_system.agents.reviewer_agent import ReviewerAgent
from datetime import datetime

class DocumentCreationWorkflow(Workflow):
    """
    Orchestrates the document creation process:
    Plan -> Draft -> Review -> Compile
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="Document Creation Workflow",
            description="Generates a full document from project metadata.",
            input_schema=ProjectMetadata,
            **kwargs
        )
        
        # Initialize Agents
        self.planner = PlannerAgent()
        self.author = AuthorAgent()
        self.reviewer = ReviewerAgent()

    def run(self, input: ProjectMetadata, run_id: Optional[str] = None, **kwargs) -> FinalDocument:
        """
        Executes the full document creation pipeline.
        """
        # Generate a job_id for this run if not present in input context (or generate new one)
        current_job_id = run_id or f"job-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        logger.info(f"Starting job {current_job_id} for project: {input.project_name}")
        
        # 1. Plan
        logger.info("Step 1: Planning...")
        
        document_plan = None
        if input.template_name:
            from maas_document_system.app.ui_templates import get_template
            from maas_document_system.schemas.document_plan import PlanItem, DocumentPlan
            
            logger.info(f"Using template: {input.template_name}")
            template = get_template(input.template_name)
            
            if template:
                plan_items = []
                for i, section in enumerate(template.sections):
                    # Create a PlanItem for each section in the template
                    # Use instructions provided in template or fallback to title/content context
                    desc_prompt = f"Draft section '{section.title}'. "
                    if section.instructions:
                        desc_prompt += f"Instructions: {section.instructions}. "
                    desc_prompt += f"Context content: {section.content[:200]}..." # Provide snippet as context
                    
                    plan_items.append(PlanItem(
                        section_id=f"sec-{i+1}", 
                        title=section.title, 
                        description_prompt=desc_prompt, 
                        hierarchy_level=1, 
                        order_index=i
                    ))
                
                document_plan = DocumentPlan(job_id=current_job_id, outline=plan_items)
                logger.info(f"Plan created from template with {len(plan_items)} sections.")
            else:
                logger.warning(f"Template {input.template_name} not found. Falling back to Planner Agent.")
        
        if not document_plan:
            # Pass job_id explicitly to Planner Agent
            document_plan = self.planner.create_plan(job_id=current_job_id, metadata=input)
            logger.info(f"Plan created with {len(document_plan.outline)} sections.")

        # 2. Draft
        logger.info("Step 2: Drafting...")
        drafted_sections: List[SectionContent] = []
        for item in document_plan.outline:
            logger.info(f"Drafting section: {item.title}")
            section = self.author.write_section(item, plan_id=document_plan.job_id)
            drafted_sections.append(section)

        # 3. Review
        logger.info("Step 3: Reviewing...")
        final_sections: List[SectionContent] = []
        for section in drafted_sections:
            logger.info(f"Reviewing section: {section.title}")
            # Call the reviewer's public API. ReviewerAgent exposes `review_content`
            # which returns a ReviewResult with fields `is_approved` and `feedback`.
            review_result = self.reviewer.review_content(section.title, section.content_md, section.hierarchy_level)

            # Simple logic: If approved, keep it. If not, we keep it but mark it (MVP)
            # In a real system, we would loop back to AuthorAgent here.
            if getattr(review_result, "is_approved", False):
                updated_section = section.model_copy(update={"status": SectionStatus.REVIEWED})
            else:
                updated_section = section.model_copy(update={"status": SectionStatus.FAILED_VALIDATION})
                logger.warning(f"Section {section.title} rejected: {getattr(review_result, 'feedback', '')}")

            final_sections.append(updated_section)

        # 4. Compile
        logger.info("Step 4: Compiling...")
        full_content = f"# {input.project_name}\n\n"
        for section in final_sections:
            full_content += f"{section.content_md}\n\n"
            
        # Save to file
        import os
        output_dir = os.path.join(os.getcwd(), "outputs", current_job_id)
        os.makedirs(output_dir, exist_ok=True)
        markdown_path = os.path.join(output_dir, "final.md")
        
        with open(markdown_path, "w") as f:
            f.write(full_content)

        final_doc = FinalDocument(
           job_id=current_job_id,
           total_sections=len(final_sections),
           markdown_path=markdown_path,
           generated_at=datetime.utcnow()
        )
        
        logger.info("Job completed successfully.")
        return final_doc
