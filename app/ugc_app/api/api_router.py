from fastapi import APIRouter
from ugc_app.api.v1.v1_router import v1_router

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)
