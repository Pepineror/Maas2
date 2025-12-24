from typing import Any, AsyncIterator, Dict, Iterator, List, Optional
from agno.models.base import Model
from agno.models.response import ModelResponse
from pydantic import BaseModel

class MockModel(Model):
    """
    A Mock Model that simulates LLM responses for testing purposes.
    It returns deterministic mock data compatible with the expected output schema.
    """
    id: str = "mock-model"
    name: str = "MockModel"
    provider: str = "MockProvider"

    def invoke(self, *args, **kwargs) -> ModelResponse:
        """
        Simulates a synchronous call to the LLM.
        """
        from agno.models.response import ModelResponse

        # Determine output based on expected schema or default behavior
        # In a real mock, we might inspect messages to determine the response.
        # Here we just return a valid empty structure or predefined mock.
        
        # We need to minimally satisfy the contract.
        return ModelResponse(content="Mock response content")

    async def ainvoke(self, *args, **kwargs) -> ModelResponse:
        """Async version of invoke."""
        return self.invoke(*args, **kwargs)

    def invoke_stream(self, *args, **kwargs) -> Iterator[ModelResponse]:
        """Simulates streaming response."""
        yield self.invoke(*args, **kwargs)

    async def ainvoke_stream(self, *args, **kwargs) -> AsyncIterator[ModelResponse]:
        """Async version of invoke_stream."""
        yield self.invoke(*args, **kwargs)

    def _parse_provider_response(self, response: Any, **kwargs) -> ModelResponse:
        return response

    def _parse_provider_response_delta(self, response: Any) -> ModelResponse:
        return response
