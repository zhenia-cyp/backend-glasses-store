from pathlib import Path
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
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    ASYNC_DATABASE_URL: str # postgresql+asyncpg://postgres:postgres@postgres:5432/postgres
    SYNC_DATABASE_URL: str # postgresql://postgres:postgres@postgres:5432/postgres

    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_SECRET_KEY: str
    ALGORITHM: str
    TOKEN_KEY: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    SESSION_SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()