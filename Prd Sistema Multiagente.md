Prd – Sistema Multiagente Para Evaluación De Viabilidad De Proyectos (acno/agno)
Product Requirements Document (PRD)
1. Visión del producto

El producto propuesto es una plataforma de generación documental inteligente, basada en un sistema multiagente (MAAS) nativo de Agno, diseñada para automatizar de extremo a extremo la elaboración del expediente de viabilidad de proyectos en contextos institucionales y empresariales.

El sistema no se limita a la generación de texto: modela el proceso real de trabajo de una consultoría, incorporando planificación, redacción, validación normativa, control de calidad, trazabilidad y auditoría. Cada documento generado es el resultado de un flujo controlado, reproducible y verificable.

La visión a largo plazo es convertir esta plataforma en un activo institucional estratégico, capaz de:

Preservar conocimiento metodológico (plantillas, normas, buenas prácticas).

Reducir dependencia de consultorías externas.

Acelerar la toma de decisiones estratégicas.

Garantizar homogeneidad y calidad documental entre proyectos.

Desarrollar un sistema de software multiagente, basado en el framework Agno (ACNO), capaz de generar automáticamente el expediente completo de viabilidad de un proyecto, compuesto por más de 30 documentos técnicos, jurídicos, económicos y organizativos, a partir de plantillas normadas y datos reales almacenados en sistemas existentes.

El sistema sustituye, acelera y estandariza el trabajo tradicional de consultoría, garantizando trazabilidad, auditabilidad, coherencia normativa y reducción significativa de tiempo y costos.

2. Problema a resolver

Los procesos actuales de evaluación de viabilidad de proyectos presentan problemas estructurales:

2.1 Problemas operativos

Elaboración manual de documentos extensos y repetitivos.

Dependencia de especialistas escasos (económicos, jurídicos, técnicos).

Alta probabilidad de errores humanos y omisiones.

2.2 Problemas económicos

Costos elevados por contratación de consultorías externas.

Retrasos que impactan cronogramas de inversión.

2.3 Problemas de gobernanza

Falta de trazabilidad clara entre datos fuente, análisis y conclusiones.

Dificultad para auditar decisiones a posteriori.

Inconsistencias entre expedientes de distintos proyectos.

El problema no es la ausencia de metodologías, sino la dificultad para aplicarlas de forma sistemática y reproducible.

Actualmente, la evaluación de viabilidad de proyectos:

Requiere consultorías externas costosas.

Involucra procesos manuales largos (semanas o meses).

Carece de estandarización fuerte entre proyectos.

Presenta baja trazabilidad entre datos fuente, análisis y conclusiones.

Existe además una gran cantidad de plantillas y metodologías ya definidas, pero su aplicación es manual y propensa a errores.

3. Objetivos del producto
Objetivo general

Automatizar la creación del expediente de viabilidad de proyectos mediante un sistema multiagente basado en IA, manteniendo cumplimiento normativo, trazabilidad y calidad técnica.

Objetivos específicos

Generar documentos extensos (10–20+ páginas) a partir de plantillas oficiales.

Conectarse a sistemas existentes para obtener datos del proyecto.

Validar automáticamente cada sección contra reglas y fuentes.

Registrar auditoría completa del proceso de generación.

Entregar al usuario un expediente final estructurado y versionado.

4. Usuarios y stakeholders
Usuarios finales

Equipos técnicos de evaluación de proyectos

Analistas económicos

Especialistas jurídicos

Direcciones institucionales

Stakeholders

Institución propietaria de las metodologías

Área de informatización

Área jurídica

Dirección estratégica

5. Alcance del producto
Incluido

Generación automática de documentos de viabilidad.

Uso de plantillas SIC y metodologías existentes.

Integración con sistemas de datos del proyecto.

Auditoría y versionado.

Validación multiagente.

Excluido (fase inicial)

Aprobación legal definitiva automática.

Firma digital institucional.

Sustitución total del experto humano (siempre existe escalado).

6. Arquitectura funcional (alto nivel)

La arquitectura sigue el paradigma Agno-native, priorizando simplicidad, control y trazabilidad sobre la distribución innecesaria.

6.1 Principios arquitectónicos

Orquestación centralizada: un único Workflow controla el ciclo de vida del documento.

Agentes cognitivos especializados: cada agente cumple un rol humano claro.

Contratos de datos estrictos: todo intercambio se realiza mediante esquemas validados.

Estado controlado: el borrador del documento vive en la memoria del Workflow.

Escalabilidad lógica: el sistema escala por número de documentos, no por complejidad infraestructural.

6.2 Justificación de Agno

Agno permite:

Modelar flujos complejos sin microservicios.

Integrar RAG y Tools de forma nativa.

Controlar bucles, reintentos y memoria.

Reducir latencia y costos de operación.

7. Modelo de agentes en detalle

El sistema está compuesto por agentes especializados que reproducen el flujo de trabajo humano de una consultoría de viabilidad.

7.1 Planner Agent (Agente Planificador)

Responsabilidades:

Analizar el tipo, alcance y complejidad del proyecto.

Determinar el conjunto de documentos requeridos.

Seleccionar las plantillas normativas aplicables.

Definir el orden de generación y dependencias.

Inputs:

Metadatos del proyecto.

Tipo de inversión / iniciativa.

Normativas aplicables.

Outputs:

Plan documental estructurado.

Lista de documentos y secciones.

Reglas de validación por sección.

7.2 Author Agent (Agente Redactor)

Responsabilidades:

Generar el contenido de cada sección.

Integrar datos reales del proyecto.

Aplicar plantillas y estilos formales.

Mantener coherencia entre secciones.

Inputs:

Plantilla de la sección.

Datos recuperados del proyecto.

Contexto normativo (RAG).

Estado actual del documento.

Outputs:

Contenido redactado de la sección.

Referencias a fuentes utilizadas.

Justificación técnica de resultados.

7.3 Reviewer Agent (Agente Revisor)

Responsabilidades:

Validar cumplimiento normativo.

Detectar inconsistencias técnicas o lógicas.

Verificar trazabilidad de datos.

Solicitar correcciones o aprobar secciones.

Inputs:

Contenido generado.

Reglas normativas.

Historial de intentos previos.

Outputs:

Estado de aprobación (aprobado / corrección / rechazo).

Comentarios estructurados.

Indicadores de calidad.

7.4 Orchestrator Workflow (Agno Workflow)

Responsabilidades:

Coordinar la interacción entre agentes.

Controlar bucles de generación–revisión.

Gestionar memoria y estado del documento.

Compilar el expediente final.

Inputs:

Solicitud del usuario.

Configuración del sistema.

Outputs:

Expediente completo.

Registro de auditoría.

Métricas del proceso.

7.5 Tooling & RAG Layer

Responsabilidades:

Acceso a datos estructurados.

Recuperación de normativa y plantillas.

Cacheo de información frecuente.

Inputs:

Consultas de agentes.

Outputs:

Datos validados.

Contexto recuperado.

8. Flujo funcional

El usuario solicita la evaluación de viabilidad del proyecto.

El Planner Agent analiza metadatos y define el plan documental.

El Workflow inicializa el estado del expediente.

Para cada documento y sección:

El Author Agent genera contenido.

El Reviewer Agent valida.

El Workflow decide aprobar, iterar o escalar.

El Workflow compila el expediente final.

Se entrega el resultado junto con auditoría completa.

9. Contratos de datos por agente (Schemas)

Los contratos de datos garantizan interoperabilidad, trazabilidad y control de calidad entre agentes.

9.1 Schema – ProjectMetadata

project_id

nombre_proyecto

tipo_proyecto

alcance

normativas_aplicables

fuentes_datos

9.2 Schema – DocumentPlan

document_id

nombre_documento

plantilla_id

secciones[]

dependencias[]

9.3 Schema – SectionRequest

section_id

document_id

contexto_normativo

datos_proyecto

intento

9.4 Schema – SectionContent

section_id

content

referencias_fuente[]

version

9.5 Schema – ReviewResult

section_id

estado (aprobado | correccion | rechazo)

observaciones

score_calidad

10. Estados del documento y máquina de estados

El expediente y cada sección siguen una máquina de estados explícita.

Estados de sección

CREATED: sección definida pero no generada.

GENERATED: contenido generado por Author Agent.

UNDER_REVIEW: en validación por Reviewer Agent.

APPROVED: sección aprobada.

REJECTED: sección rechazada definitivamente.

ESCALATED: requiere revisión humana.

Transiciones

CREATED → GENERATED

GENERATED → UNDER_REVIEW

UNDER_REVIEW → APPROVED | CORRECTION | REJECTED

CORRECTION → GENERATED

REJECTED → ESCALATED

11. Política de errores y fallos controlados

El sistema adopta una política de fallo seguro y controlado.

Tipos de errores

Errores de datos: información incompleta o inconsistente.

Errores normativos: incumplimiento de reglas.

Errores de generación: incoherencia, alucinación.

Errores de integración: fallos en sistemas externos.

Estrategias

Reintentos limitados y registrados.

Fallback a caché o datos parciales.

Escalado humano automático.

Bloqueo de entrega si hay secciones críticas no aprobadas.

12. Mapa de riesgos específicos del sistema multiagente
Riesgos técnicos

Desalineación entre agentes.

Exceso de reintentos.

Latencia acumulada.

Riesgos de datos

Fuentes incompletas.

Datos desactualizados.

Riesgos de IA

Alucinaciones.

Sobreconfianza en resultados.

Riesgos operativos

Dependencia excesiva del sistema.

Falta de capacitación de usuarios.

Mitigaciones

Reviewer Agent estricto.

Auditoría obligatoria.

Escalado humano.

Métricas continuas de calidad.

13. Roadmap

Usuario solicita evaluación de viabilidad.

Planner Agent define documentos y secciones.

Por cada sección:

Author genera contenido.

Reviewer valida contra reglas.

Se itera hasta aprobación o máximo de intentos.

Workflow compila el expediente final.

Sistema entrega documentos + auditoría.

8. Requisitos funcionales
8.1 Generación documental

RF-01
El sistema debe generar expedientes de viabilidad compuestos por 30 o más documentos distintos, de acuerdo con el tipo de proyecto.

RF-02
Cada documento debe estructurarse obligatoriamente a partir de plantillas normativas oficiales, respetando secciones, orden y estilo.

RF-03
Cada sección de cada documento debe generarse, revisarse y aprobarse de forma independiente, garantizando control granular de calidad.

8.2 Integración de datos

RF-04
El sistema debe integrarse con sistemas legados y repositorios de datos mediante herramientas (Tools) desacopladas.

RF-05
El acceso a datos debe implementar mecanismos de caché, evitando consultas redundantes y mejorando el rendimiento.

8.3 Control de calidad y validación

RF-06
Toda sección generada debe pasar por un Reviewer Agent antes de considerarse válida.

RF-07
El sistema debe limitar automáticamente el número máximo de reintentos de generación por sección.

8.4 Auditoría y gobierno del proceso

RF-08
Debe existir un registro de auditoría completo, por sección y por documento, incluyendo decisiones y responsables (agentes).

RF-09
Cada afirmación relevante del documento debe estar trazable a una fuente de datos o normativa.

8.5 Intervención humana

RF-10
El sistema debe permitir el escalado a revisión humana cuando se detecten bloqueos, inconsistencias críticas o riesgos elevados.

9. Requisitos no funcionales
9.1 Calidad

Coherencia interna entre documentos y secciones.

Cumplimiento normativo verificable.

Reproducibilidad del proceso de generación.

9.2 Rendimiento

Generación del expediente completo en horas, no en semanas.

Capacidad de procesar múltiples proyectos en paralelo.

9.3 Seguridad

Control de acceso basado en roles.

Compartimentación de la información por proyecto y unidad organizativa.

Protección de datos sensibles.

9.4 Trazabilidad y auditoría

Persistencia de estados, versiones y decisiones.

Posibilidad de reconstruir el proceso completo a posteriori.

10. Contratos de datos por agente (Schemas)

Los contratos de datos definen estructuras formales de intercambio entre agentes, garantizando interoperabilidad y control.

10.1 ProjectMetadata

project_id

nombre_proyecto

tipo_proyecto

alcance

normativas_aplicables

fuentes_datos

10.2 DocumentPlan

document_id

nombre_documento

plantilla_id

secciones[]

dependencias[]

10.3 SectionRequest

section_id

document_id

contexto_normativo

datos_proyecto

intento

10.4 SectionContent

section_id

content

referencias_fuente[]

version

10.5 ReviewResult

section_id

estado (aprobado | corrección | rechazo)

observaciones

score_calidad

11. Estados del documento y máquina de estados

El sistema implementa una máquina de estados explícita tanto a nivel de sección como de documento.

11.1 Estados de una sección

CREATED: sección definida, aún no generada.

GENERATED: contenido generado por el Author Agent.

UNDER_REVIEW: en revisión por el Reviewer Agent.

APPROVED: sección validada y aceptada.

REJECTED: sección rechazada de forma definitiva.

ESCALATED: requiere intervención humana.

11.2 Transiciones permitidas

CREATED → GENERATED

GENERATED → UNDER_REVIEW

UNDER_REVIEW → APPROVED | CORRECTION | REJECTED

CORRECTION → GENERATED

REJECTED → ESCALATED

12. Política de errores y fallos controlados

El sistema adopta una política de fallo seguro, priorizando la integridad del expediente sobre la completitud automática.

12.1 Tipos de errores

Errores de datos: información incompleta o inconsistente.

Errores normativos: incumplimiento de reglas formales.

Errores de generación: incoherencias, alucinaciones.

Errores de integración: fallos en sistemas externos.

12.2 Estrategias de mitigación

Reintentos limitados y registrados.

Uso de datos en caché o valores parciales.

Escalado automático a revisión humana.

Bloqueo de entrega si existen secciones críticas no aprobadas.

13. Mapa de riesgos específicos del sistema multiagente
13.1 Riesgos técnicos

Desalineación entre agentes.

Incremento excesivo de iteraciones.

Latencia acumulada en flujos largos.

13.2 Riesgos de datos

Fuentes incompletas o desactualizadas.

Inconsistencias entre sistemas.

13.3 Riesgos asociados a IA

Alucinaciones en texto generado.

Sobreconfianza en resultados automáticos.

13.4 Riesgos operativos

Dependencia excesiva del sistema.

Uso indebido sin capacitación adecuada.

13.5 Medidas de mitigación

Reviewer Agent con validaciones estrictas.

Auditoría obligatoria y persistente.

Intervención humana en puntos críticos.

Métricas continuas de calidad y desempeño.
