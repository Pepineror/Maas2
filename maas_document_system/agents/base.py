import os
import logging
from agno.models.base import Model

logger = logging.getLogger(__name__)


def get_model() -> Model:
    """Factory to return the configured LLM model.

    Production-ready behavior (per requested logic):
    1. If `OPENWEBUI_BASE_URL` is configured, prefer using OpenWebUI as
       an OpenAI-compatible endpoint (the app will treat it like OpenAI).
    2. Else if `OPENAI_API_KEY` is set, use OpenAIChat against OpenAI or
       any configured `OPENAI_API_BASE` proxy.
    3. If neither is configured, raise a RuntimeError (do not fall back to
       mocks in production-focused mode).

    The function returns an instance compatible with `agno.models.base.Model`.
    """
    openwebui_base = os.getenv("OPENWEBUI_BASE_URL")
    openwebui_model = os.getenv("OPENWEBUI_MODEL_ID", os.getenv("OPENAI_MODEL_ID", "gpt-4o"))

    # 1) Prefer OpenWebUI if provided (treated as OpenAI-compatible API)
    if openwebui_base:
        try:
            from agno.models.openai import OpenAIChat

            # ensure base URL ends without slash and point to /v1 if not present
            base = openwebui_base.rstrip("/")
            # many OpenWebUI/OpenAI-compatible proxies expose /v1 endpoints
            if not base.endswith("/v1"):
                base = f"{base}/v1"

            api_key = os.getenv("OPENAI_API_KEY", "")
            logger.info("Using OpenWebUI at %s as OpenAI-compatible endpoint", base)
            return OpenAIChat(id=openwebui_model, api_key=api_key or None, base_url=base)
        except Exception as e:
            logger.error("Failed to initialize OpenWebUI adapter: %s", e)

    # 2) Fallback to OpenAI if configured
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from agno.models.openai import OpenAIChat
            model_id = os.getenv("OPENAI_MODEL_ID", "gpt-4o")
            base = os.getenv("OPENAI_API_BASE")
            return OpenAIChat(id=model_id, api_key=api_key, base_url=base)
        except Exception as e:
            logger.error("Failed to initialize OpenAI adapter: %s", e)

    # 3) Production-focused: do not return mocks silently — fail fast
    raise RuntimeError(
        "No LLM provider configured. Set OPENWEBUI_BASE_URL or OPENAI_API_KEY for production usage."
    )
