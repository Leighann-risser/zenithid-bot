from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    DATABASE_URL: str
    REDIS_URL: str
    # আপনার অ্যাডমিন আইডি এখানে ডিফল্ট হিসেবে সেট করা হয়েছে
    ADMIN_ID: int = 1864128377 
    SHEERID_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()