"""
Application settings and configuration.
"""
from __future__ import annotations
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List, Optional

BACKEND_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    """Main application settings."""
    APP_NAME: str = "ClinIQ"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    SECRET_KEY: str = Field("3f8a2e1b9c4d7f0e6a5b2c8d1e4f7a0b3c6d9e2f5a8b1c4d7e0f3a6b9c2d5e8f", description="Secret key for JWT")
    DATABASE_URL: str = Field("sqlite+aiosqlite:///./cliniq.db", description="Database connection string")
    SARVAM_API_KEY: Optional[str] = None
    GLM_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None   # retained for config compatibility
    CORS_ORIGINS: List[str] = ["*"]
    BACKEND_PORT: int = 8056
    FRONTEND_PORT: int = 3056
    NGROK_INSPECT_PORT: int = 4056

    model_config = SettingsConfigDict(
        env_file=(
            str(BACKEND_DIR / ".env"),
            ".env",
            "backend/.env",
        ),
        env_file_encoding="utf-8",
        extra="ignore"
    )

def get_settings() -> Settings:
    """Return the application settings."""
    return Settings()

