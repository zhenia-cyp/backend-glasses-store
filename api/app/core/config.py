from pydantic_settings import BaseSettings
import os

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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()