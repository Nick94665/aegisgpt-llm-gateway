import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET: str = os.getenv("JWT_SECRET", "changemeplease")
    AUDIT_DB_URL: str = os.getenv("AUDIT_DB_URL", "sqlite+aiosqlite:///./audit.db")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "mock")  # "openai", "vertex", or "mock"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

settings = Settings()
