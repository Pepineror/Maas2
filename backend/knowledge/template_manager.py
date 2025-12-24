import os
from typing import Dict, Optional
from backend.core.config import settings
from backend.core.logging import logger

class TemplateManager:
    """
    Manages document templates stored in the knowledge base.
    """
    def __init__(self, templates_dir: Optional[str] = None):
        # Default to backend/knowledge/templates
        self.templates_dir = templates_dir or os.path.join(
            os.path.dirname(__file__), "templates"
        )
        self.templates: Dict[str, str] = {}
        self._load_templates()

    def _load_templates(self):
        """Loads all .md templates from the templates directory."""
        if not os.path.exists(self.templates_dir):
            logger.warning(f"Templates directory not found: {self.templates_dir}")
            os.makedirs(self.templates_dir, exist_ok=True)
            return

        for filename in os.listdir(self.templates_dir):
            if filename.endswith(".md"):
                template_name = filename[:-3]
                path = os.path.join(self.templates_dir, filename)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        self.templates[template_name] = f.read()
                    logger.info(f"Loaded template: {template_name}")
                except Exception as e:
                    logger.error(f"Failed to load template {filename}: {e}")

    def get_template(self, name: str) -> Optional[str]:
        """Retrieves a template by name."""
        return self.templates.get(name)

    def list_templates(self) -> Dict[str, str]:
        """Returns a list of all available templates and their names."""
        return {name: content[:100] + "..." for name, content in self.templates.items()}

# Singleton instance
template_manager = TemplateManager()
