🧱 Estructura del Proyecto (Agno-Native)
maas_document_system/
│
├── app/
│   ├── main.py
│   ├── settings.py
│
├── agents/
│   ├── planner_agent.py
│   ├── author_agent.py
│   ├── reviewer_agent.py
│
├── workflows/
│   └── document_creation_workflow.py
│
├── schemas/
│   ├── document_outline.py
│   ├── section_content.py
│   ├── reviewer_feedback.py
│   ├── audit_log.py
│   └── final_document.py
│
├── tools/
│   ├── get_viability_data.py
│   └── fetch_source_text.py
│
├── knowledge/
│   └── sic_templates/
│       ├── sic_01.md
│       ├── sic_02.md
│       └── ...
│
└── requirements.txt

📐 Schemas (Contratos de Datos)
schemas/audit_log.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AuditLogEntry(BaseModel):
    attempt_number: int
    timestamp: datetime
    status: str  # OK | RECHAZADO
    reviewer_feedback: Optional[str] = None
    citation_check_result: bool

schemas/reviewer_feedback.py
from pydantic import BaseModel

class ReviewerFeedback(BaseModel):
    status: str  # OK | RECHAZADO
    reviewer_feedback: str
    citation_check_result: bool

schemas/section_content.py
from pydantic import BaseModel
from typing import List
from .audit_log import AuditLogEntry

class SectionContent(BaseModel):
    section_id: str
    section_title: str
    content_markdown: str
    source_references: List[str]
    audit_log: List[AuditLogEntry] = []

schemas/document_outline.py
from pydantic import BaseModel
from typing import List

class OutlineSection(BaseModel):
    section_id: str
    title: str
    description: str

class DocumentOutline(BaseModel):
    template_id: str
    sections: List[OutlineSection]

schemas/final_document.py
from pydantic import BaseModel
from typing import List
from .section_content import SectionContent

class FinalDocumentSchema(BaseModel):
    document_id: str
    project_id: str
    template_id: str
    revision: str
    created_at: str
    sections: List[SectionContent]
    final_status: str  # SIN_OBSERVACIONES | CON_OBSERVACIONES | FALLIDO

🤖 Agentes
agents/planner_agent.py
from agno import Agent
from schemas.document_outline import DocumentOutline

PlannerAgent = Agent(
    name="PlannerAgent",
    role="Arquitecto de Estructura",
    instructions="""
    Genera únicamente la estructura del documento según la plantilla SIC indicada.
    No redactes contenido.
    Devuelve un DocumentOutline válido.
    """,
    output_schema=DocumentOutline,
)

agents/author_agent.py
from agno import Agent
from schemas.section_content import SectionContent
from tools.get_viability_data import get_viability_data

AuthorAgent = Agent(
    name="AuthorAgent",
    role="Redactor Técnico",
    instructions="""
    Redacta solo la sección asignada.
    Si recibes reviewer_feedback:
    - Aplica el Principio de Delta: modifica solo lo indicado.
    - No reescribas el resto.
    Cita siempre las fuentes usadas.
    """,
    tools=[get_viability_data],
    output_schema=SectionContent,
)

agents/reviewer_agent.py
from agno import Agent
from schemas.reviewer_feedback import ReviewerFeedback
from tools.fetch_source_text import fetch_source_text

ReviewerAgent = Agent(
    name="ReviewerAgent",
    role="Auditor SIC",
    instructions="""
    Evalúa cumplimiento SIC.
    Cita regla exacta violada.
    Verifica coherencia semántica entre contenido y fuentes.
    """,
    tools=[fetch_source_text],
    output_schema=ReviewerFeedback,
)

🛠️ Tools
tools/get_viability_data.py
def get_viability_data(project_id: str) -> dict:
    """
    1. Verifica caché (Redis).
    2. Si no existe, consulta API legada.
    3. Normaliza datos.
    4. Registra métricas (cache_hit, latency).
    """
    return {
        "source_id": f"viability:{project_id}",
        "data": "datos normalizados de viabilidad"
    }

tools/fetch_source_text.py
def fetch_source_text(ref_id: str) -> str:
    """
    Recupera el texto original de una fuente citada
    para verificación semántica.
    """
    return "texto fuente original"

⚙️ Workflow Central
workflows/document_creation_workflow.py
from agno import Workflow
from datetime import datetime
from schemas.final_document import FinalDocumentSchema
from schemas.audit_log import AuditLogEntry

MAX_ATTEMPTS = 4

class DocumentCreationWorkflow(Workflow):

    def __init__(self, planner, author, reviewer):
        self.planner = planner
        self.author = author
        self.reviewer = reviewer

    def run(self, topic, project_id, template_id):
        outline = self.planner.run(
            f"Tema: {topic}, Plantilla: {template_id}"
        )

        final_doc = FinalDocumentSchema(
            document_id="AUTO",
            project_id=project_id,
            template_id=template_id,
            revision="A",
            created_at=str(datetime.utcnow()),
            sections=[],
            final_status="EN_PROCESO"
        )

        for section in outline.sections:
            feedback = ""
            for attempt in range(1, MAX_ATTEMPTS + 1):
                section_content = self.author.run({
                    "section": section,
                    "previous_feedback": feedback
                })

                review = self.reviewer.run(section_content)

                log = AuditLogEntry(
                    attempt_number=attempt,
                    timestamp=datetime.utcnow(),
                    status=review.status,
                    reviewer_feedback=review.reviewer_feedback,
                    citation_check_result=review.citation_check_result
                )

                section_content.audit_log.append(log)

                if review.status == "OK":
                    final_doc.sections.append(section_content)
                    break

                feedback = review.reviewer_feedback

            else:
                final_doc.final_status = "FALLIDO"
                return final_doc

        final_doc.final_status = "SIN_OBSERVACIONES"
        return final_doc

▶️ app/main.py
from agents.planner_agent import PlannerAgent
from agents.author_agent import AuthorAgent
from agents.reviewer_agent import ReviewerAgent
from workflows.document_creation_workflow import DocumentCreationWorkflow

workflow = DocumentCreationWorkflow(
    planner=PlannerAgent,
    author=AuthorAgent,
    reviewer=ReviewerAgent
)

result = workflow.run(
    topic="Evaluación de viabilidad del proyecto X",
    project_id="N24UE15",
    template_id="SIC-03"
)

print(result.json(indent=2))

