from pathlib import Path
from typing import Annotated, Literal, Any

from pydantic import ClickHouseDsn, DirectoryPath, SecretStr, field_validator, MongoDsn
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR: DirectoryPath = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    # mongo_host: str
    # mongo_port: int
    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'INFO'
    json_logs: bool = True
    debug: bool = False
    mongo_dsn: MongoDsn | str = 'mongodb://mongoadmin:mongoadmin@localhost:27017'
    # MONGO_DATABASE: str = 'movie'
    # MONGO_COLLECTION_LIKE: str = 'like'
    # MONGO_COLLECTION_BOOKMARK: str = 'bookmark'
    # MONGO_COLLECTION_REVIEW: str = 'review'
    # MONGO_COLLECTION_REVIEW_RATING: str = 'review_rating'
    # MONGO_COLLECTION_MOVIES: str = 'movies'

    # @field_validator('mongo_dsn')
    # def build_mongo_dsn(
    #     cls, value: MongoDsn | None, info: ValidationInfo
    # ) -> Annotated[str, MongoDsn]:  # type: ignore
    #     if not value:
    #         value = MongoDsn.build(
    #             scheme='mongodb',
    #             username=info.data.get('mongo_user', ''),
    #             password=info.data.get('mongo_password', ''),
    #             host=info.data['mongo_host'],
    #             port=info.data['mongo_port'],
    #             path=f"{info.data['mongo_database'] or ''}",
    #         )
    #     return str(value)

    model_config = SettingsConfigDict(env_file=PROJECT_DIR / '.env')


settings = Settings()
