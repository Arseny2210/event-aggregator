from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/event_aggregator"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "change-this-to-a-random-secret-key"
    environment: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:3000,http://localhost:8000"
    db_echo: bool = False
    db_pool_size: int = 5
    db_max_overflow: int = 10
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    upload_dir: str = "./uploads"
    max_upload_size_bytes: int = 10_485_760
    default_import_category_id: str = ""
    import_batch_size: int = 100
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_use_tls: bool = True
    smtp_from_address: str = "noreply@example.com"
    notification_max_retries: int = 3
    openapi_docs_enabled: bool = True
    openapi_schema_enabled: bool = True

    @model_validator(mode="after")
    def _validate_secret_key(self) -> "Settings":
        if (
            self.environment == "production"
            and self.secret_key == "change-this-to-a-random-secret-key"
        ):
            raise ValueError("SECRET_KEY must be set to a secure random value in production")
        return self

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
