from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "sqlite:///./nestegg.db"
    secret_key: str = "your-secret-key-here"
    admin_password: str = "admin123"
    user_password: str = "user123"
    access_token_expire_minutes: int = 10080
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()