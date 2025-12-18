import pytest
from unittest.mock import patch, mock_open
import os
from maas_document_system.app.ui_templates import get_template, list_templates, DocumentTemplate, PANTIAS_DIR

# Mock content based on real file structure seen
MOCK_TEMPLATE_CONTENT = """Plantilla Mock
I. Encabezado
General info...
1.0 Some section
II. Contenido
More content...
## Section X
Content X
"""

def test_list_templates():
    with patch("os.path.exists", return_value=True):
        with patch("os.listdir", return_value=["temp1.md", "temp2.TXT", "temp3.md"]):
            templates = list_templates()
            assert len(templates) == 2
            assert "temp1.md" in templates
            assert "temp3.md" in templates

def test_get_template_found():
    with patch("os.path.exists", return_value=True): # For file existence check
        with patch("builtins.open", mock_open(read_data=MOCK_TEMPLATE_CONTENT)):
             template = get_template("temp1.md")
             assert isinstance(template, DocumentTemplate)
             assert template.filename == "temp1.md"
             assert template.metadata.name == "Plantilla Mock"
             # Verify sections
             # 'Plantilla Mock' is first line, but not a section title (unless we change logic)
             # Current logic splits by startswith.
             # 'Plantilla Mock' -> 'I. Encabezado'
             # First section 'General' gets 'Plantilla Mock' (as line 0 is stripped? no line 0 is used as title logic)
             # Wait, logic: title = lines[0]. loop starts lines.
             # line[0] 'Plantilla Mock' -> appended to current_section_lines.
             # line[1] 'I. Encabezado' -> New section 'I. Encabezado'
             
             assert len(template.sections) > 1
             assert template.sections[1].title == "I. Encabezado"

def test_get_template_not_found():
    with patch("os.path.exists", return_value=False):
        template = get_template("missing.md")
        assert template is None
