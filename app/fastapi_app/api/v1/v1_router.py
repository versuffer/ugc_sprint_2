from fastapi import APIRouter

from app.fastapi_app.api.v1.metrics.metrics_router import metrics_router
from app.fastapi_app.api.v1.ugc.ugc_router import ugc_router

v1_router = APIRouter(prefix='/v1')
v1_router.include_router(metrics_router)
v1_router.include_router(ugc_router)
