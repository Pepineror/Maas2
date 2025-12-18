Sad – Sistema Multiagente De Generación Documental De Viabilidad (agno/acno)
Software Architecture Document (SAD)
1. Introducción
1.1 Propósito del documento

Este documento describe la arquitectura de software del sistema multiagente para la generación automática del expediente de viabilidad de proyectos, basado en el framework Agno (ACNO). El SAD sirve como referencia técnica oficial para desarrollo, despliegue, operación, auditoría y evolución del sistema.

1.2 Alcance

El documento cubre:

Visión arquitectónica general

Diagramas C4 (Contexto, Contenedores, Componentes)

Descripción de componentes y responsabilidades

Flujos principales

Decisiones arquitectónicas clave

Requisitos de calidad y riesgos

2. Visión general del sistema

El sistema implementa un Modelo Multiagente como Servicio (MAAS) para reproducir el flujo de trabajo de una consultoría de evaluación de viabilidad, automatizando la planificación, redacción, validación y compilación documental.

Principios rectores:

Orquestación centralizada

Agentes especializados

Estado controlado

Trazabilidad total

Fallo seguro

3. Diagrama C4 – Nivel 1 (Contexto)
3.1 Descripción

Actor principal:

Usuario institucional (equipo técnico / decisor)

Sistemas externos:

Sistemas de información del proyecto (legados)

Repositorio normativo / plantillas SIC

Servicios de modelos de lenguaje (LLM)

Relación: El usuario solicita la evaluación de viabilidad. El sistema se conecta a fuentes de datos internas y normativas para generar y entregar el expediente completo.

4. Diagrama C4 – Nivel 2 (Contenedores)
4.1 Contenedores principales

UI / API Gateway

Punto de entrada al sistema

Autenticación, autorización y control de acceso

Application Server (Agno Runtime)

Aloja el Workflow y los agentes

Persistence Layer

Base de datos relacional (PostgreSQL)

Almacenamiento de objetos (documentos)

Caché (Redis)

Vector Database

Indexación de plantillas y normativas

LLM Proxy / Services

Acceso controlado a modelos de lenguaje

5. Diagrama C4 – Nivel 3 (Componentes)
5.1 Componentes del Application Server
Componente	Responsabilidad principal
DocumentCreationWorkflow	Orquestación del proceso completo
PlannerAgent	Planificación documental
AuthorAgent	Generación de contenido
ReviewerAgent	Validación normativa y técnica
Tool Layer	Acceso a datos y servicios
Audit Manager	Registro de auditoría
6. Descripción de componentes
6.1 DocumentCreationWorkflow

Controla estados y transiciones

Aplica política de reintentos

Compila el expediente final

6.2 Planner Agent

Analiza metadatos del proyecto

Define documentos, secciones y reglas

6.3 Author Agent

Genera contenido conforme a plantillas

Integra datos reales del proyecto

6.4 Reviewer Agent

Verifica cumplimiento normativo

Detecta inconsistencias y alucinaciones

6.5 Tool Layer

Encapsula integraciones

Implementa caché y validaciones

7. Flujos arquitectónicos clave
7.1 Flujo de generación por sección

Definición de sección (Planner)

Generación de contenido (Author)

Revisión y validación (Reviewer)

Aprobación / Corrección / Escalado

8. Decisiones arquitectónicas
Decisión	Justificación
Agno-native	Reduce complejidad y latencia
Orquestación central	Facilita control y auditoría
RAG normativo	Reduce alucinaciones
Contratos tipados	Garantiza calidad e interoperabilidad
9. Requisitos de calidad

Seguridad: control de acceso y cifrado

Trazabilidad: auditoría por sección

Escalabilidad: paralelismo por proyecto

Mantenibilidad: agentes desacoplados

10. Riesgos arquitectónicos y mitigación
Riesgo	Mitigación
Alucinaciones	Reviewer + RAG + bloqueo
Datos incompletos	Validación + escalado
Costos LLM	Tiering y caché
11. Cumplimiento y gobernanza

Separación IA / decisión humana

Auditoría persistente

Revisión manual obligatoria en casos críticos

12. Evolución de la arquitectura

Incorporación de nuevos agentes

Integración con firma digital

Automatización parcial de aprobación

13. Conclusiones

La arquitectura propuesta es robusta, viable y alineada con contextos institucionales, permitiendo la automatización segura y gobernada de procesos críticos de evaluación de viabilidad.
