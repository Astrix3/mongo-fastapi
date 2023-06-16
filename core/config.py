from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class CommonSettings(BaseSettings):
    APP_NAME: str = "KIMO"
    DEBUG_MODE: bool = False

class ServerSettings(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 8000

class DatabaseSettings(BaseSettings):
    db_name: str = "kimo"
    db_url: str = "mongodb://localhost:27017/"
    class Config:
        env_prefix = "DB_"

class Settings(CommonSettings, DatabaseSettings, ServerSettings):
    pass

settings = Settings()