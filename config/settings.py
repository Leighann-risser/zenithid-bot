from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    DATABASE_URL: str
    REDIS_URL: str
    SHEERID_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()