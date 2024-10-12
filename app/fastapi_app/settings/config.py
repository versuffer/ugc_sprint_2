from pathlib import Path
from typing import Annotated, Literal, Any

from pydantic import ClickHouseDsn, DirectoryPath, SecretStr, field_validator, MongoDsn
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR: DirectoryPath = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    APP_TITLE: str = 'UGC Srint 2'
    APP_DESCRIPTION: str = 'Default description'
    DEBUG: bool = False
    ENABLE_AUTH: bool = False
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'INFO'
    JSON_LOGS: bool = True
    AUTH_SERVICE_URL: str
    AUTH_SERVICE_API: dict = {'verify_token': '/api/v1/auth/verify/access_token'}
    SERVICES: list[str] = ['front']
    USER_ID_FIELD: str = 'login'
    KAFKA_HOST: str
    KAFKA_PORT: str
    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: SecretStr
    CLICKHOUSE_DB: str
    CLICKHOUSE_DSN: ClickHouseDsn | str = ''
    SENTRY_DSN: str
    MONGO_DSN: MongoDsn | str = ''
    MONGO_DATABASE: str = 'movie'
    MONGO_COLLECTION_LIKE: str = 'like'
    MONGO_COLLECTION_BOOKMARK: str = 'bookmark'
    MONGO_COLLECTION_REVIEW: str = 'review'
    MONGO_COLLECTION_REVIEW_RATING: str = 'review_rating'
    MONGO_COLLECTION_MOVIES: str = 'movies'

    @field_validator('CLICKHOUSE_DSN')
    def build_clickhouse_dsn(
        cls, value: ClickHouseDsn | None, info: ValidationInfo
    ) -> Annotated[str, ClickHouseDsn]:  # type: ignore
        if not value:
            value = ClickHouseDsn.build(
                scheme='clickhouse+native',
                username=info.data['CLICKHOUSE_USER'],
                password=info.data['CLICKHOUSE_PASSWORD'].get_secret_value(),
                host=info.data['CLICKHOUSE_HOST'],
                port=info.data['CLICKHOUSE_PORT'],
                path=f"{info.data['CLICKHOUSE_DB'] or ''}",
            )
        return str(value)
    #
    # @field_validator('MONGO_DSN')
    # def build_clickhouse_dsn(
    #     cls, value: MongoDsn | None, info: ValidationInfo
    # ) -> Annotated[str, MongoDsn]:  # type: ignore
    #     if not value:
    #         value = MongoDsn.build(
    #             scheme='mongodb',
    #             username=info.data.get('MONGO_USER', ''),
    #             password=info.data.get('MONGO_PASSWORD', ''),
    #             host=info.data['MONGO_HOST'],
    #             port=info.data['MONGO_PORT'],
    #             path=f"{info.data['MONGO_DATABASE'] or ''}",
    #         )
    #     return str(value)

    model_config = SettingsConfigDict(env_file=PROJECT_DIR / '.env')


settings = Settings()
