import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.fastapi_app.schemas.api.v1.schemas import LikeSchema, ReviewSchema, BookmarkSchema
from app.fastapi_app.services.repositories.mongo.models import Bookmark
from app.fastapi_app.services.ugc.ugc_service import UgcService

ugc_router = APIRouter(prefix='/ugc')


@ugc_router.get('/like/{film_id}', response_model=list[LikeSchema])
async def like(
    film_id: uuid.UUID,
    service: UgcService = Depends(),
):
    return service.get_likes(film_id=film_id)


@ugc_router.post(
    "/like/{user_id}/{film_id}",
    summary="Добавить оценку фильма",
    # response_model=response_models.RatingGetModel,
    tags=["Likes"],
    # dependencies=[Depends(jwt_user_verify)],
)
async def like_add(
    # data: response_models.RatingAddModel,
    user_id: uuid.UUID,
    film_id: uuid.UUID,
    score: int,
    service: UgcService = Depends(),
):

    item = await service.add_likes(user_id, film_id, score)

    return item


@ugc_router.get('/review', response_model=list[ReviewSchema])
async def review(
    film_id: uuid.UUID,
    service: UgcService = Depends(),
):
    return service.get_reviews(film_id=film_id)


@ugc_router.get('/bookmark', response_model=list[BookmarkSchema])
async def bookmark(
    film_id: uuid.UUID,
    service: UgcService = Depends(),
):
    return service.get_bookmarks(film_id=film_id)
