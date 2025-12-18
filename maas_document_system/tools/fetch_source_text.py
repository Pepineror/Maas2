import hashlib
from agno.tools import Toolkit
from maas_document_system.schemas.tool_outputs import SourceContent

class SourceTextTools(Toolkit):
    def __init__(self):
        super().__init__(name="source_text_tools")
        self.register(self.fetch_text_from_source)

    def fetch_text_from_source(self, source_id: str) -> SourceContent:
        """
        Fetches text content from a given source ID.
        Currently a stub returning mock content.
        
        TODO: Implement actual RAG indexing hook here.
        TODO: Connect to Document Store.

        Args:
            source_id (str): ID of the source document.

        Returns:
            SourceContent: The content with hash and metadata.
        """
        # Mock content
        mock_text = f"This is the content for source {source_id}.\nIt contains technical specifications and requirements."
        content_hash = hashlib.sha256(mock_text.encode("utf-8")).hexdigest()
        
        return SourceContent(
            source_id=source_id,
            content_text=mock_text,
            sha256_hash=content_hash,
            metadata={"author": "System Stub", "type": "mock"}
        )
