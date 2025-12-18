Arquitectura propuesta — a partir del PRD (Agno-native MAAS)

Abajo tienes una arquitectura técnica completa y accionable, alineada punto por punto con el PRD que subiste. Incluye: diagrama lógico, componentes, contratos de datos (Pydantic), especificación de Tools/APIs, flujo de ejecución (secuencia), despliegue infra, seguridad, observabilidad, modos de fallo y roadmap técnico para el MVP → producción.

1. Visión general de la arquitectura

Paradigma: Agno-native (un Workflow central orquesta agentes Planner, Author, Reviewer).

Estado y datos estructurados: todos los intercambios son contratos Pydantic (no texto libre).

Acceso a conocimiento: RAG / Vector DB para plantillas SIC y reglas.

Tools: funciones Python (no microservicios HTTP internos) que encapsulan la lógica de caché/ETL y acceso a fuentes.

Persistencia: Postgres (metadatos, historial, audit log), Redis (cache), y Object Storage (documentos finales, artefactos).

LLMs: separación por tiers (autor rápido vs revisor potente).

2. Diagrama lógico (texto / componentes)
[User UI / API] 
    |
    v
[API Gateway / App Server]
    |
    v
[DocumentCreationWorkflow (Agno)]
    |---> Planner Agent (local)  <--- RAG? (consulta plantillas)
    |---> Author Agent ---------------> Tools: get_viability_data()
    |---> Reviewer Agent -------------> RAG(VectorDB: SIC) + fetch_source_text()
    |
    v
[Persistence]
    - Postgres (FinalDocumentSchema, ProjectMetadata, AuditLog, states)
    - Redis (cache de get_viability_data)
    - Object Storage (markdown/pdf/docx)
    - Vector DB (plantillas SIC indexadas)
    |
    v
[LLM Services] (internal LLM proxy) 

3. Componentes principales (detallado)
3.1 API / UI layer

Endpoints REST/GraphQL para:

POST /v1/documents/generate -> iniciar workflow (topic, project_id, template_id)

GET /v1/documents/{doc_id} -> estado + descarga

GET /v1/projects/{project_id} -> metadatos

Autenticación (JWT / OIDC) y ACL (roles, provincia).

3.2 DocumentCreationWorkflow (Agno)

Clase central que:

Recibe request, inicializa FinalDocumentSchema.

Llama a planner.execute(...) para obtener DocumentPlan.

Itera secciones, llama author.execute() y reviewer.execute() con bucle de reintentos (max 4).

Registra AuditLogEntry por intento.

Compila resultado y lo persiste (Postgres + Object Storage).

3.3 Planner Agent

Genera DocumentPlan (lista de secciones, reglas por sección).

Usa system prompt + templates metadata (desde vector DB o DB de plantillas).

3.4 Author Agent

Produce SectionContent (Markdown), añade referencias_fuente[].

Llama get_viability_data(project_id) tool para datos del proyecto.

Debe ejecutar self-check minimal (verifica que cumplió la regla citada en feedback anterior).

3.5 Reviewer Agent

Usa RAG (Vector DB indexado con plantillas SIC) para localizar reglas aplicables.

Llama fetch_source_text(ref_id) para obtener texto fuente completo.

Realiza verificación semántica entre SectionContent y las fuentes citadas.

Devuelve ReviewResult (OK/REJECT + correction_notes estructurado).

3.6 Tools (encapsulados)

get_viability_data(project_id):

Strategy: Redis cache -> legacy API -> ETL transform -> persist en cache.

Registra métricas: cache_hit, legacy_api_call, latency.

fetch_source_text(ref_id):

Recupera texto completo de plantillas/soportes para verificación semántica.

Tooling adicional: render_to_pdf(markdown), store_document(blob).

3.7 Persistencia & Search

Postgres: FinalDocumentSchema, DocumentPlan, ProjectMetadata, AuditLogs, states.

Object Storage (S3 compatible): Markdown/DOCX/PDF y versiones.

Vector DB (FAISS/Chroma/Weaviate): plantillas SIC + fragmentos con metadatos (rule_id).

Redis: cache de get_viability_data.

3.8 LLM Layer

LLM proxy que permite:

Selección de modelo por rol.

Rate-limiting, token accounting, fallback.

Capa de seguridad (sanitize inputs/outputs).

4. Contratos (Pydantic) — ejemplos (código)
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProjectMetadata(BaseModel):
    project_id: str
    nombre_proyecto: str
    tipo_proyecto: str
    alcance: str
    normativas_aplicables: List[str]
    fuentes_datos: List[str]

class SectionRequest(BaseModel):
    section_id: str
    document_id: str
    contexto_normativo: List[str]
    datos_proyecto: dict
    intento: int

class AuditLogEntry(BaseModel):
    attempt_number: int
    timestamp: datetime
    status: str  # "OK"|"RECHAZO"
    reviewer_feedback: Optional[str]
    citation_check_result: Optional[bool]

class SectionContent(BaseModel):
    section_id: str
    content_markdown: str
    referencias_fuente: List[str]
    version: int
    audit_log: List[AuditLogEntry] = []

class ReviewResult(BaseModel):
    section_id: str
    estado: str  # "aprobado"|"correccion"|"rechazo"
    observaciones: Optional[str]
    score_calidad: Optional[float]

5. Flujo de ejecución — secuencia (por sección)

Workflow toma DocumentPlan.

Para section in DocumentPlan.secciones:

Request = SectionRequest(...) (attempt=1)

section_draft = author.execute(request)

review = reviewer.execute(section_draft, template_id)

registrar AuditLogEntry.

Si review.estado == "aprobado" → persistir SectionContent (APPROVED).

Si correccion → request.intento += 1 y pasar review.observaciones como previous_feedback al author.

Si intento > MAX_ATTEMPTS → marcar ESCALATED, notificar humano.

Al finalizar todas secciones aprobadas → compile() produce FinalDocumentSchema.

render_to_pdf() y store_document().

6. Especificación Tools / API internas (contratos)
get_viability_data(project_id: str) -> dict

Inputs: project_id

Side effects: consulta Redis; si miss -> legacy API -> transforma datos -> guarda cache.

Metrics: cache_hit_rate, legacy_api_calls, avg_latency.

Errors: raise DataUnavailableError

fetch_source_text(ref_id: str) -> str

Inputs: ref_id (ej. sic_01:rule_4A)

Return: texto completo de la regla/plantilla.

Uso: reviewer para verificación semántica.

7. Máquina de estados (persistencia)

Tabla section_states:

section_id, document_id, state, attempt_count, last_updated, last_reviewer_id, current_version_id.

Transiciones atomizadas dentro de Workflow con persistencia ACID (Postgres transaction).

8. Seguridad & gobernanza

Autenticación: OIDC / LDAP / SSO institucional.

Autorización: roles (admin, editor, reviewer, auditor) + ACL por province_id (acceso solo a proyectos de la provincia).

Encriptado: TLS in transit; at-rest encryption para Postgres/object storage.

Auditoría: immutable audit_log con firma (hash) por versión del SectionContent.

Acceso a LLM: logs sanitizados, red team review de prompts.

9. Observabilidad y métricas

KPIs (implementables desde inicio):

avg_attempts_per_section

approval_rate_per_attempt

cache_hit_rate

hallucination_rate = % secciones donde citation_check_result == False

workflow_latency por documento

Tracing: OpenTelemetry traces desde API → Workflow → LLM calls.

Alerting: si avg_attempts_per_section > 2.5 o cache_hit_rate < 40%.

10. Escalado y rendimiento

Escala horizontal del app server / worker nodes (cada Workflow instancia puede correr en un worker).

Vector DB y Postgres escalados según tamaño de index/throughput.

LLM proxies con pooling y multi-tier models (usar modelo más barato para Author, costlier para Reviewer).

Redis para alta tasa de lecturas de datos de proyectos.

11. Política de fallos y recuperación

Reintentos transaccionales: Workflow reintenta operaciones idempotentes (persistencia).

Checkpoints: guardar estado después de completar cada sección (permite resume).

Escalado humano automático: crear ticket/alerta con payload + audit_log si attempts >= 4.

Backup & restore: backups snapshots Postgres y Vector DB nightly.

12. Riesgos técnicos (ligados a diseño) y mitigaciones (rápidas)

Alucinaciones → mitigación: mandatory referencias_fuente + Reviewer semántico + bloqueo de aprobación si citation_check_result == False.

Datos inconsistentes → mitigación: get_viability_data() valida esquema y devuelve missing_fields → reviewer/author notificado.

Costo LLM → mitigación: tiering de modelos, caching de prompts/respuestas, presupuesto por proyecto.

13. Roadmap técnico (tareas, priorización MVP)

Fase 0 — Setup

Repositorio, CI, infra básica (Postgres, Redis, Object Storage), LLM proxy.

Fase 1 — MVP (4–8 semanas)

Implementar Pydantic schemas.

Implementar Workflow in-memory + Planner (static templates 1–3).

Implementar Author y Reviewer con same LLM (prototipo).

Implement Tools: get_viability_data (mock), fetch_source_text (local files).

Persistencia básica + audit log.

Basic UI/API to start workflow and view document status.

Metrics: attempts, approval rate.

Fase 2 — Piloto (8–16 semanas)

Indexar plantillas en Vector DB.

Integrar Redis + legacy API real.

Introducir Reviewer LLM potente (tiering).

Render PDF/DOCX, storage versioning.

Implement ACL por provincia.

Fase 3 — Producción

Harden infra (k8s), backup/DR, monitoring avanzado, SLA de LLM, optimizaciones de costos.

14. Artefactos entregables de la arquitectura (qué te doy si quieres)

SAD (Software Architecture Document) con diagramas (C4) y especificaciones de infra.

Spec de APIs y Tools (OpenAPI).

Código base: Pydantic models + pseudocódigo Agno Workflow + stubs de Agents.

Plantilla de prompts (Planner/Author/Reviewer) y tests E2E para MVP.

15. Pseudocódigo del Workflow (detallado)
class DocumentCreationWorkflow(Workflow):
    MAX_ATTEMPTS = 4

    def __init__(self, planner, author, reviewer, storage, metrics):
        self.planner = planner
        self.author = author
        self.reviewer = reviewer
        self.storage = storage
        self.metrics = metrics

    def run(self, project_meta: ProjectMetadata, template_id: str):
        plan: DocumentPlan = self.planner.execute(project_meta, template_id)
        final_doc = FinalDocumentSchema.from_plan(plan, metadata=project_meta)
        for doc in plan.documents:
            for section in doc.secciones:
                attempt = 0
                while attempt < self.MAX_ATTEMPTS:
                    attempt += 1
                    req = SectionRequest(..., intento=attempt)
                    draft: SectionContent = self.author.execute(req)
                    review: ReviewResult = self.reviewer.execute(draft, template_id)
                    audit = AuditLogEntry(attempt_number=attempt, timestamp=now(), status=review.estado, reviewer_feedback=review.observaciones)
                    draft.audit_log.append(audit)
                    self.storage.save_temporary_section(draft)
                    if review.estado == "aprobado":
                        final_doc.append_section(draft)
                        break
                    else:
                        if attempt >= self.MAX_ATTEMPTS:
                            self.escalate_to_human(draft)
                            final_doc.mark_section_escalated(draft)
                            break
                        # prepare feedback for next attempt
                        last_feedback = review.observaciones
                        req.add_feedback(last_feedback)
        compiled = self.compile(final_doc)
        self.storage.persist_final_document(compiled)
        return compiled

