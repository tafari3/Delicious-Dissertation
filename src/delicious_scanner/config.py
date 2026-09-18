from __future__ import annotations

import secrets
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///.data/scanner.db"
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"
    environment: str = "development"
    auth_enabled: bool = True
    auth_username: str = "scanner-admin"
    auth_password_hash: str = (
        "pbkdf2_sha256$600000$GcjSEWDwVrFFoPV1IQ9lBwY4$SzUC1H2bpgQ3i32lKeHSF8ASjfVqmjhxRU7fX80pTJA"
    )
    session_secret: str = Field(default_factory=lambda: secrets.token_urlsafe(48))
    session_ttl_seconds: int = 28_800
    secure_cookies: bool = False

    model_config = SettingsConfigDict(env_prefix="DELICIOUS_", env_file=".env", extra="ignore")

    @property
    def database_path(self) -> Path | None:
        prefix = "sqlite:///"
        if not self.database_url.startswith(prefix):
            return None
        return Path(self.database_url.removeprefix(prefix))


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
