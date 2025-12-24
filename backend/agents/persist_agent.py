import os
import json
from typing import Dict, Any
from backend.core.config import settings
from backend.core.logging import logger

class PersistAgent:
    """
    PersistAgent handles the 'Commit Tripartita':
    1. Postgres (Metadata & Status)
    2. S3/Storage (Markdown content)
    3. VectorDB (Embeddings for future RAG)
    """
    def __init__(self):
        self.output_dir = settings.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def commit_fragment(self, project_id: str, section_title: str, content: str, metadata: Dict[str, Any]):
        """
        Persists a document fragment (section).
        """
        logger.info(f"PersistAgent: Committing fragment '{section_title}' for {project_id}")
        
        # 1. Simulate Postgres Save
        # In production: db.session.add(DocumentFragment(...))
        
        # 2. Storage Save (Local Filesystem as S3 Mock)
        project_path = os.path.join(self.output_dir, project_id)
        os.makedirs(project_path, exist_ok=True)
        
        safe_title = "".join([c if c.isalnum() else "_" for c in section_title])
        fragment_file = os.path.join(project_path, f"{safe_title}.md")
        
        with open(fragment_file, "w") as f:
            f.write(content)
            
        # 3. Simulate VectorDB Indexing
        # In production: vector_db.upsert(content, metadata)
        
        logger.info(f"PersistAgent: Fragment {section_title} persisted successfully.")

    def finalize_document(self, project_id: str, full_text: str):
        """
        Saves the final consolidated document.
        """
        project_path = os.path.join(self.output_dir, project_id)
        os.makedirs(project_path, exist_ok=True)
        final_file = os.path.join(project_path, "final_document.md")
        
        with open(final_file, "w") as f:
            f.write(full_text)
        
        logger.info(f"PersistAgent: Final document for {project_id} saved at {final_file}")
        return final_file

# Singleton instance
persist_agent = PersistAgent()
