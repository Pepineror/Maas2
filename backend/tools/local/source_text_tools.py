import hashlib
from agno.tools import Toolkit
from backend.schemas.tool_outputs import SourceContent

class SourceTextTools(Toolkit):
    def __init__(self):
        super().__init__(name="source_text_tools")
        self.register(self.fetch_text_from_source)

    def fetch_text_from_source(self, source_id: str) -> SourceContent:
        """
        Fetches text content from a given source ID.
        Currently a stub returning mock content.
        
        Args:
            source_id (str): ID of the source document or URL.

        Returns:
            SourceContent: The content with hash and metadata.
        """
        # Mock content
        mock_text = f"Content retrieved from {source_id}.\nEnterprise MAAS v4.0 Source Text Extraction Tool."
        content_hash = hashlib.sha256(mock_text.encode("utf-8")).hexdigest()
        
        return SourceContent(
            source_id=source_id,
            content_text=mock_text,
            sha256_hash=content_hash,
            metadata={"source_type": "enterprise_stub"}
        )
