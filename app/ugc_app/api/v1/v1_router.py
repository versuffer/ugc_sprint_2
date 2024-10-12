from fastapi import APIRouter

from ugc_app.api.v1.ugc.ugc_router import ugc_router

v1_router = APIRouter(prefix='/v1')
v1_router.include_router(ugc_router)
