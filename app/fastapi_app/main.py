import logging
from contextlib import asynccontextmanager
from pprint import pformat

import sentry_sdk
import uvicorn
from aiokafka import AIOKafkaProducer
from clickhouse_driver import Client
from fastapi import Depends, FastAPI, Header, Request
from starlette_context import request_cycle_context

from app.clickhouse.sql import clickhouse_init_sql_queries
from app.fastapi_app.api.api_router import api_router
from app.fastapi_app.settings.config import settings
from app.fastapi_app.settings.logs import logger
from app.kafka.producers import kafka_producer


async def fastapi_context(x_request_id=Header(default='NO_REQUEST_ID')):
    data = {'request_id': x_request_id}
    with request_cycle_context(data):
        yield


sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Kafka
        bootstrap = {'bootstrap_servers': '{}:{}'.format(settings.KAFKA_HOST, settings.KAFKA_PORT)}
        kafka_producer.aio_producer = AIOKafkaProducer(**bootstrap)
        await kafka_producer.aio_producer.start()  # type: ignore

        # Clickhouse
        clickhouse_client = Client.from_url(settings.CLICKHOUSE_DSN)
        try:
            for sql in clickhouse_init_sql_queries:
                clickhouse_client.execute(sql.format(kafka_host=settings.KAFKA_HOST, kafka_port=settings.KAFKA_PORT))
        finally:
            clickhouse_client.disconnect()
        yield
    finally:
        await kafka_producer.aio_producer.stop()  # type: ignore
        logger.info('Application stopped.')


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version='1.0.0',
    debug=settings.DEBUG,
    docs_url='/',
    lifespan=lifespan,
    dependencies=[Depends(fastapi_context)],
)


@app.middleware('http')
async def sentry_request_id_middleware(request: Request, call_next):
    request_id = request.headers.get('X-Request-ID') or 'NO_REQUEST_ID'
    with sentry_sdk.configure_scope() as sentry_scope:
        sentry_scope.set_tag('request_id', request_id)

    return await call_next(request)


app.include_router(api_router)


if __name__ == "__main__":
    logger.info(f"Start server. Settings: \n{pformat(settings.dict())}")
    uvicorn.run("main:app", host="localhost", port=8000, log_level=logging.DEBUG)
