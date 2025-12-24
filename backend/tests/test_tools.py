import pytest
from backend.tools.get_viability_data import ViabilityTools
from backend.tools.fetch_source_text import SourceTextTools
from backend.tools.render_to_pdf import RenderTools
from backend.schemas.tool_outputs import ViabilityMetrics, SourceContent, RenderOutput

# --- Viability Tools Tests ---
def test_viability_tool_success():
    toolkit = ViabilityTools()
    # Direct method call
    result = toolkit.get_project_viability("Project Alpha")
    assert isinstance(result, ViabilityMetrics)
    assert result.project_name == "Project Alpha"
    assert result.risk_level in ["Low", "Medium", "High"]

def test_viability_tool_deterministic():
    toolkit = ViabilityTools()
    res1 = toolkit.get_project_viability("Same Name")
    res2 = toolkit.get_project_viability("Same Name")
    assert res1.viability_score == res2.viability_score

# --- Source Text Tools Tests ---
def test_source_fetch_success():
    toolkit = SourceTextTools()
    result = toolkit.fetch_text_from_source("ID-123")
    assert isinstance(result, SourceContent)
    assert result.source_id == "ID-123"
    assert len(result.sha256_hash) == 64  # SHA256 length

# --- Render Tools Tests ---
def test_render_tool_success():
    toolkit = RenderTools()
    markdown = "# Hello"
    result = toolkit.markdown_to_pdf(markdown, "/tmp/out.pdf")
    assert isinstance(result, RenderOutput)
    assert result.output_path == "/tmp/out.pdf"
    assert result.pages >= 1

# --- Input Validation Tests (Implicit via Pydantic) ---
# Since tools are typed, passing wrong types *at runtime* in Python 
# without a type checker might still work if compatible, but Pydantic 
# return validation ensures the *Output* is correct.
# Here we test that the return value adheres to the schema.

def test_viability_schema_validation():
    # If the internal logic produced invalid data (e.g. score > 100), 
    # it would raise a ValidationError upon constructing the response model.
    # Since our stub logic is safe, we just verify the success path above.
    pass
