from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from ugc_app.schemas.api.v1.schemas import ScoreSchema, TextReviewSchema, BookmarkSchema, CreateTextReviewSchema, \
    CreateBookmarkSchema, ReviewExtSchema, CreateScoreReviewSchema, ScoreReviewSchema
from ugc_app.services.ugc.ugc_service import UgcService

ugc_router = APIRouter()


# @ugc_router.get('/scores/{film_id}', response_model=ScoreSchema, tags=["Likes"])
# async def scores(
#     film_id: UUID,
#     service: UgcService = Depends(),
# ):
#     return await service.get_score(film_id=film_id)
#
#
# @ugc_router.post(
#     "/like/{user_id}/{film_id}",
#     summary="Добавить оценку фильма",
#     # response_model=response_models.RatingGetModel,
#     tags=["Likes"],
#     # dependencies=[Depends(jwt_user_verify)],
# )
# async def add_score(
#     user_id: UUID,
#     film_id: UUID,
#     score: int,
#     service: UgcService = Depends(),
# ):
#
#     item = await service.add_score(user_id, film_id, score)
#
#     return item


# @ugc_router.get('/review', response_model=list[ReviewSchema], tags=["Reviews"])
# async def review(
#     film_id: UUID,
#     # service: UgcService = Depends(),
# ):
#     return service.get_reviews(film_id=film_id)
#
#

@ugc_router.post('/bookmarks', response_model=BookmarkSchema, tags=["Bookmarks"])
async def add_bookmark(
    bookmark_data: CreateBookmarkSchema,
    service: UgcService = Depends(),
):
    return await service.add_bookmark(bookmark_data)


@ugc_router.get('/bookmarks/{user_id}', response_model=list[BookmarkSchema], tags=["Bookmarks"])
async def user_bookmarks(
    user_id: UUID,
    service: UgcService = Depends(),
):
    return await service.get_bookmarks(user_id=user_id)


@ugc_router.delete('/bookmarks/{user_id}/{film_id}', response_model=str, tags=["Bookmarks"])
async def delete_user_bookmark(
    user_id: UUID,
    film_id: UUID,
    service: UgcService = Depends(),
):
    if result := await service.del_bookmark(user_id=user_id, film_id=film_id):
        return JSONResponse(status_code=HTTP_200_OK, content=result)
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Bookmark not found")


@ugc_router.post('/reviews', response_model=TextReviewSchema, tags=["Reviews"])
async def add_text_review(
    text_review_data: CreateTextReviewSchema,
    service: UgcService = Depends(),
):
    if review := await service.add_text_review(text_review_data):
        return JSONResponse(
            content=jsonable_encoder(review.model_dump()),
            status_code=HTTP_201_CREATED,
            headers={"Location": f"/reviews/{review.id}"}
        )
    raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Unable to create the review. Invalid data.")


@ugc_router.get('/reviews/{film_id}', response_model=list[ReviewExtSchema], tags=["Reviews"])
async def add_text_review(
    film_id: UUID,
    service: UgcService = Depends(),
):
    return await service.get_film_reviews(film_id)


@ugc_router.put('/reviews/{review_id}/score', response_model=ScoreReviewSchema, tags=["Reviews"])
async def upsert_score_review(
    review_id: UUID,
    score_review_data: CreateScoreReviewSchema,
    service: UgcService = Depends(),
):
    return await service.upsert_score_review(review_id, score_review_data)
