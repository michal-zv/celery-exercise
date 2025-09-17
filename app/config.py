from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    app_name: str = "Celery Exercise"
    database_url: str = os.getenv("DATABASE_URL")
    upload_dir: str = os.getenv("UPLOAD_DIR", "app/uploads")

    class Config:
        env_file = ".env"

settings = Settings()