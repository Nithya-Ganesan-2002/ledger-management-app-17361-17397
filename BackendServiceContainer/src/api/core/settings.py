import os
from functools import lru_cache
from typing import List

# PUBLIC_INTERFACE
def get_env(name: str, default: str | None = None) -> str:
    """Get environment variable with optional default."""
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

class Settings:
    """Application settings loaded from environment variables."""

    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = 60  # token expiry

    # Database - must be provided by BackendServiceContainer_database
    # Note: orchestrator should set these in .env, we do not hardcode.
    DB_URL: str

    # CORS
    CORS_ALLOW_ORIGINS: List[str]

    def __init__(self) -> None:
        self.JWT_SECRET_KEY = get_env("JWT_SECRET_KEY", "change-me-in-prod")
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
        self.JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))

        # BackendServiceContainer_database integration
        self.DB_URL = get_env("DB_URL", "sqlite+aiosqlite:///./ledger.db")

        # CORS
        cors = os.getenv("CORS_ALLOW_ORIGINS", "*")
        self.CORS_ALLOW_ORIGINS = [o.strip() for o in cors.split(",") if o.strip()]

# PUBLIC_INTERFACE
@lru_cache
def get_settings() -> Settings:
    """Return application settings (cached)."""
    return Settings()
