"""Application configuration."""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# 无论从项目根还是 backend 目录启动，都从 backend 目录加载 .env
_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    """App settings from env."""

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE if _ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "通用篡改检测 API"
    debug: bool = False
    # CORS
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    # Upload
    max_upload_bytes: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: frozenset[str] = frozenset(
        {"jpg", "jpeg", "png", "bmp", "pdf", "tiff", "tif", "webp", "gif"}
    )
    # LangChain / AI (optional)
    openai_api_key: str | None = None
    enable_ai_chain: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
