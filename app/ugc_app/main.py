from contextlib import asynccontextmanager

import uvicorn
from api.api_router import api_router
from beanie import init_beanie
from fastapi import Depends, FastAPI, Header
from motor.motor_asyncio import AsyncIOMotorClient
from services.repositories.mongo.models import (
    BookmarkModel,
    ScoreModel,
    ScoreReviewModel,
    TextReviewModel,
)
from settings.config import settings
from starlette_context import request_cycle_context


async def fastapi_context(x_request_id=Header(default="NO_REQUEST_ID")):
    data = {"request_id": x_request_id}
    with request_cycle_context(data):
        yield


@asynccontextmanager
async def lifespan(app: FastAPI):

    mongo_client = AsyncIOMotorClient(settings.mongo_dsn)
    await init_beanie(
        database=mongo_client[settings.mongo_db],
        document_models=[BookmarkModel, ScoreModel, TextReviewModel, ScoreReviewModel],
    )
    yield
    mongo_client.close()


app = FastAPI(
    title="UGC - 2",
    description="description",
    version="1.0.0",
    debug=settings.debug,
    docs_url="/docs",
    root_path="/ugc_app",
    lifespan=lifespan,
    dependencies=[Depends(fastapi_context)],
)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000)
