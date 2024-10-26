from api.v1.v1_router import v1_router
from fastapi import APIRouter

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)
