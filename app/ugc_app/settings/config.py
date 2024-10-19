from pathlib import Path
from typing import Literal

from pydantic import DirectoryPath, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR: DirectoryPath = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    json_logs: bool = True
    debug: bool = False
    mongo_dsn: MongoDsn | str = "mongodb://localhost:27017"
    mongo_db: str = 'MoviesDB'

    model_config = SettingsConfigDict(env_file=PROJECT_DIR / ".env")


settings = Settings()
