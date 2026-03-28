from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ENVIRONMENT = Literal["development", "staging", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    """Application settings loaded from environment and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    shutdown_timeout: int = 5

    env: ENVIRONMENT = "development"
    log_level: LogLevel = "INFO"
    port: int = 8000

    app_name: str = "Career Conversations AI"
    app_description: str = (
        "RAG-based career assistant built with FastAPI, Qdrant, Redis, and Gradio."
    )
    app_version: str = "1.0.0"
    welcome_message: str = ""

    app_owner: str
    avatar_path: str | None = None

    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_embeddings_model: str = "text-embedding-3-small"

    pushover_token: str
    pushover_user: str

    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str = "career-conversations-collection"

    upstash_redis_rest_url: str
    upstash_redis_rest_token: str

    @property
    def is_production(self) -> bool:
        return self.env == "production"

    @model_validator(mode="after")
    def set_welcome_message(self) -> "Settings":
        if not self.welcome_message:
            self.welcome_message = (
                f"Hi, I'm {self.app_owner}'s AI agent. Welcome! "
                "Ask me anything about my background, skills, and experience."
            )

        return self


settings = Settings()
