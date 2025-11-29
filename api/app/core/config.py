from pathlib import Path
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
API_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = API_DIR / ".env"

class Settings(BaseSettings):

    HOST: str = "localhost"
    PORT: int = 8000
    DEBUG: bool = True
    RELOAD: bool = True

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    ASYNC_DATABASE_URL: str | None = None
    SYNC_DATABASE_URL: str | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Автоматично визначаємо хост для Docker
        db_host = os.getenv("POSTGRES_HOST", self.POSTGRES_HOST)
        # Якщо працюємо в Docker, використовуємо ім'я сервісу
        if os.path.exists("/.dockerenv") and db_host == "localhost":
            db_host = "db"
        
        # Якщо URL не вказано явно, будуємо його
        if not self.ASYNC_DATABASE_URL:
            self.ASYNC_DATABASE_URL = (
                f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{db_host}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        if not self.SYNC_DATABASE_URL:
            self.SYNC_DATABASE_URL = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{db_host}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )

    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_SECRET_KEY: str
    ALGORITHM: str
    TOKEN_KEY: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    SESSION_SECRET_KEY: str

    EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES: int
    EMAIL_VERIFICATION_URL: str

    OAUTH_SUCCESS_REDIRECT_URL: str = "http://localhost:3000/auth/success"
    OAUTH_FAILURE_REDIRECT_URL: str = "http://localhost:3000/auth/error"

    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_USE_TLS: bool

    REDIS_PORT: str
    REDIS_URL: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()