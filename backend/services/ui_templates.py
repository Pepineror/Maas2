import os
import logging
from typing import List, Optional
from backend.schemas.template_contracts import DocumentTemplate, TemplateMetadata, TemplateSection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Resolving path relative to this file
# This file is in backend/app/
# knowledge is in backend/knowledge/
# Path: ../knowledge/templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PANTIAS_DIR = os.path.abspath(os.path.join(BASE_DIR, "../knowledge/templates"))

def get_pantias_dir() -> str:
    """Returns the resolved path to pantias directory."""
    return PANTIAS_DIR

def list_templates() -> List[str]:
    """Lists available template filenames."""
    if not os.path.exists(PANTIAS_DIR):
        logger.warning(f"Pantias directory not found at {PANTIAS_DIR}")
        return []
    
    return [f for f in os.listdir(PANTIAS_DIR) if f.lower().endswith(".md")]

def get_template(filename: str) -> Optional[DocumentTemplate]:
    """
    Reads a template file and returns a structured DocumentTemplate.
    """
    filepath = os.path.join(PANTIAS_DIR, filename)
    if not os.path.exists(filepath):
        logger.error(f"Template file not found: {filepath}")
        return None
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Basic parsing strategy:
        # First line is usually title
        lines = content.splitlines()
        title = lines[0].strip("# ").strip() if lines else filename
        
        # Metadata inference
        metadata = TemplateMetadata(
            id=filename.replace(".md", "").replace(" ", "_").lower(),
            name=title,
            description="Imported from Markdown Template"
        )
        
        # Simple Section Parsing (Just one big section for now or split by ##)
        # We can enhance this to parse headers
        sections = []
        current_section_title = "General"
        current_section_lines = []
        
        for line in lines:
            if line.strip().startswith("## ") or line.strip().startswith("I. ") or line.strip().startswith("II. "):
                if current_section_lines:
                    sections.append(TemplateSection(
                        title=current_section_title,
                        content="\n".join(current_section_lines)
                    ))
                    current_section_lines = []
                current_section_title = line.strip("# ").strip()
            current_section_lines.append(line)
            
        if current_section_lines:
             sections.append(TemplateSection(
                title=current_section_title,
                content="\n".join(current_section_lines)
            ))

        return DocumentTemplate(
            filename=filename,
            metadata=metadata,
            raw_content=content,
            sections=sections
        )

    except Exception as e:
        logger.error(f"Error reading template {filename}: {e}")
        return None
