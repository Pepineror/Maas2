Especificación del Flujo de Trabajo
OpenWebUI → MAAS Multiagente (Agno) → OpenWebUI

Sistema de Generación Automática de Documentos de Viabilidad

1. Propósito del Documento

Este documento describe de forma detallada el flujo de trabajo completo para la generación automatizada de informes de viabilidad de proyectos mediante un sistema multiagente (MAAS) implementado con Agno, utilizando OpenWebUI como interfaz única de usuario.

El objetivo es definir con precisión:

La interacción entre OpenWebUI y el MAAS.

La secuencia de ejecución interna del sistema multiagente.

Los mecanismos de entrega de resultados al usuario final.

Los estados, responsabilidades y contratos involucrados.

2. Actores del Sistema
Actor	Descripción
Usuario Final	Solicita la generación de documentos desde OpenWebUI.
OpenWebUI	Interfaz de usuario y cliente de herramientas.
MAAS (Agno)	Motor cognitivo multiagente encargado de la generación documental.
Repositorio de Salida	Almacenamiento temporal o persistente de documentos generados.
3. Rol de OpenWebUI en la Arquitectura

OpenWebUI actúa exclusivamente como:

Interfaz de interacción humana.

Orquestador de intención del usuario.

Cliente de herramientas externas (Tool Server).

OpenWebUI no ejecuta lógica de generación, validación ni control de calidad.

4. Descripción General del Flujo
Usuario
  ↓
OpenWebUI
  ↓ (Tool Invocation)
MAAS – Document Server (Agno)
  ↓
Workflow Multiagente
  ↓
Generación y Validación
  ↓
Repositorio de Documentos
  ↓
OpenWebUI
  ↓
Usuario

5. Flujo de Trabajo Detallado
5.1 Inicio del Proceso (OpenWebUI)

El usuario ingresa una solicitud del tipo:

“Generar todos los informes de viabilidad del proyecto X”.

OpenWebUI interpreta la intención y la traduce en una invocación de herramienta.

5.2 Invocación del MAAS (Tool Call)

OpenWebUI realiza una llamada al servidor MAAS con el siguiente contrato:

{
  "tool": "generate_project_documents",
  "arguments": {
    "project_id": "N24UE15",
    "template_set": ["SIC-01", "SIC-03", "SIC-14"],
    "topic": "Evaluación integral de viabilidad",
    "output_formats": ["pdf", "docx", "md"]
  }
}

5.3 Recepción y Preparación del MAAS

Al recibir la solicitud, el MAAS:

Valida el payload.

Genera un identificador único de ejecución (job_id).

Inicializa el estado del proceso.

Lanza el DocumentCreationWorkflow.

Estado inicial:

CREATED → RUNNING

5.4 Ejecución Interna del Workflow (Agno Native)

Por cada plantilla solicitada, el MAAS ejecuta el flujo completo:

5.4.1 Planificación

PlannerAgent genera el esquema estructural del documento (DocumentOutline).

Se definen secciones, jerarquía y alcance.

5.4.2 Redacción

AuthorAgent redacta cada sección individualmente.

Utiliza RAG y herramientas de datos (ETL/Caché).

Declara fuentes utilizadas.

5.4.3 Validación y Corrección

ReviewerAgent valida:

Cumplimiento de reglas SIC.

Coherencia semántica con fuentes.

Aplica bucle de corrección con un máximo de 4 intentos.

Registra auditoría por sección.

5.4.4 Compilación

Se ensamblan todas las secciones aprobadas.

Se genera el FinalDocumentSchema.

5.5 Generación de Artefactos

Una vez aprobado el contenido:

Se generan los documentos en los formatos solicitados.

Se guardan en el repositorio de salida:

/outputs/{job_id}/{template_id}/


Archivos típicos:

Documento PDF

Documento DOCX

Versión Markdown

Metadata JSON de auditoría

5.6 Finalización del Proceso

El MAAS actualiza el estado final:

RUNNING → COMPLETED


o, en caso de errores parciales:

RUNNING → PARTIAL_SUCCESS

5.7 Respuesta a OpenWebUI

El MAAS devuelve a OpenWebUI:

{
  "job_id": "JOB-2025-09-0012",
  "status": "COMPLETED",
  "quality_status": "SIN_OBSERVACIONES",
  "documents": [
    {
      "template": "SIC-03",
      "format": "pdf",
      "download_url": "/download/JOB-2025-09-0012/SIC-03.pdf"
    }
  ]
}

5.8 Presentación al Usuario (OpenWebUI)

OpenWebUI:

Muestra el estado del proceso.

Lista los documentos generados.

Permite descarga directa.

No expone detalles internos del workflow.

6. Estados del Proceso
Estados del Job MAAS
Estado	Descripción
CREATED	Solicitud aceptada
RUNNING	Generación en curso
PARTIAL_SUCCESS	Algunos documentos fallaron
FAILED	Fallo crítico
COMPLETED	Proceso exitoso
7. Principios de Diseño Clave

Desacoplamiento total UI / lógica cognitiva.

Ejecución controlada y auditable.

Resiliencia mediante reintentos limitados.

Entrega batch de documentos.

Escalabilidad horizontal del MAAS.

8. Consideraciones de Seguridad y Escalabilidad

OpenWebUI no accede a datos internos del MAAS.

El MAAS controla acceso a herramientas y datos.

Jobs largos se ejecutan de forma asíncrona.

El sistema soporta múltiples usuarios concurrentes.

9. Conclusión

Este flujo de trabajo define una arquitectura robusta, escalable y alineada con estándares enterprise, donde OpenWebUI actúa como interfaz única de usuario y el MAAS implementado con Agno ejecuta toda la lógica cognitiva, garantizando calidad, trazabilidad y control total del proceso de generación documental.
