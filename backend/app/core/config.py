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
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
