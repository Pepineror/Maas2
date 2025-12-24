import os
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """
    Centralized configuration for MAAS Document System.
    Uses pydantic-settings to validate environment variables.
    """
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

    # Backend
    PROJECT_NAME: str = "Enterprise MAAS Document System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    PORT: int = 8000
    DEBUG: bool = False

    # LLM Providers
    OPENAI_API_KEY: Optional[str] = Field(None, description="API Key for OpenAI")
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Database & Cache
    DATABASE_URL: str = Field(
        default="sqlite:///storage/sessions.db",
        description="PostgreSQL URL for production, SQLite for local dev"
    )
    REDIS_URL: str = "redis://redis:6379/0"
    VECTOR_DB_URL: str = "http://qdrant:6333"

    # External Integrations
    REDMINE_BASE_URL: Optional[str] = "http://cidiia.uce.edu.do"
    REDMINE_API_KEY: Optional[str] = None
    
    # OpenWebUI Integration
    OPENWEBUI_BASE_URL: Optional[str] = "http://openwebui:3000"
    OPENWEBUI_API_KEY: Optional[str] = None

    # Security
    JWT_SECRET: str = Field(default="secret", min_length=8)
    MAAS_API_KEY_SECRET: Optional[str] = None

    # Monitoring (AgentOps)
    AGENTOPS_API_KEY: Optional[str] = None
    ENABLE_TELEMETRY: bool = True

    # Storage Paths
    DOCS_DIR: str = "storage/docs"
    OUTPUT_DIR: str = "storage/outputs"

# Create singleton instance
settings = Settings()
