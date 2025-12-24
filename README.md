# 🚀 Enterprise MAAS v4.0 (Agno Powered)

## Overview
MAAS (Multi-Agent Application Server) is an autonomous system for generating complex technical and financial documentation (SICs/APIs). Powered by the **Agno** framework, it utilizes a parallel DAG architecture to ensure performance, resiliency, and high-quality outputs.

### Key Features
*   **Autonomous Workflows**: Transition from sequential steps to robust, parallelized DAGs.
*   **Tiered Model Routing**: Optimized latency and cost by routing tasks to the appropriate LLM tier (Flash vs. Quality vs. Reasoning).
*   **RealTimeCache**: Redis-backed caching for project metrics and visibility data.
*   **Commit Tripartita**: Guaranteed persistence across Postgres (Metadata), Storage (Prose), and VectorDB (Context).
*   **Tool Server Integration**: Exposes agents and specialized tools (Redmine, Viability) for consumption by OpenWebUI.

## 📁 Project Structure
```text
backend/
├── agents/           # Specialized Agents (Planner, Author, Reviewer, Ingestor, etc.)
├── core/             # Centralized Config, Monitoring, and LLM Gateway
├── knowledge/        # Markdown Templates and TemplateManager
├── schemas/          # Strong-typed Pydantic Models for all contracts
├── tools/            # Integration (Redmine, OpenWebUI) and Local Toolkits
└── workflows/        # Orchestration logic (DocumentCreationWorkflow)
```

## 🛠️ Usage

### Installation
```bash
uv pip install .
```

### Running the Server
```bash
./backend/start.sh
```

### Deployment (Docker)
```bash
docker compose up -d --build
```

## 📄 Documentation Generation (SICs)
MAAS is specifically optimized to generate Codelco pre-investment documents (SIC 01 to 22) by extracting data from Redmine/SAP/P6 and applying autonomous Micro-Planning.

---
**Gerencia de Proyectos - Codelco**
*Empowered by Agno Framework*
