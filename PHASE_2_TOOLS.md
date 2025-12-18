# Phase 2 - Tools Implementation Context

## Strict Rules
- **No Business Logic**: Tools are dumb fetches or transformers.
- **No LLM**: Do not use LLMs inside tools.
- **Typed Outputs**: ALL tools must return a Pydantic Schema, NEVER a raw dict.
- **Auditable**: Inputs and outputs must be loggable.

## Tool Contracts
### 1. Viability Tool
- **Input**: `project_name: str`
- **Output**: `ViabilityMetrics` (ROI, score, risk_level)
- **Stub**: Return realistic mock data deterministically based on project name hash or simple logic.

### 2. Source Fetcher
- **Input**: `source_id: str`
- **Output**: `SourceContent` (text, source_metadata, sha256_hash)
- **RAG Status**: None. Add `TODO: Indexing hook`.

### 3. PDF Renderer
- **Input**: `markdown: str`
- **Output**: `RenderOutput` (path, size_bytes, pages_count)
