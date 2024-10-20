from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from schemas.api.v1.schemas import (
    BookmarkSchema,
    CreateBookmarkSchema,
    CreateScoreReviewSchema,
    CreateScoreSchema,
    CreateTextReviewSchema,
    ReviewExtSchema,
    ScoreReviewSchema,
    ScoreSchema,
    TextReviewSchema,
)
from services.ugc.ugc_service import UgcService

ugc_router = APIRouter()


@ugc_router.get("/scores/{film_id}", response_model=ScoreSchema, tags=["Scores"])
async def scores(
    film_id: UUID,
    service: UgcService = Depends(),
):
    return await service.get_score(film_id=film_id)


@ugc_router.put(
    "/scores/{user_id}/{film_id}",
    summary="Изменить иил добавить оценку фильма",
    response_model=CreateScoreSchema,
    tags=["Scores"],
)
async def upsert_score(
    user_id: UUID,
    film_id: UUID,
    score: int = Query(..., ge=0, le=10),
    service: UgcService = Depends(),
):

    item = await service.upsert_score(user_id, film_id, score)

    return item


@ugc_router.delete("/scores/{user_id}/{film_id}", tags=["Scores"])
async def delete_user_film_score(
    user_id: UUID,
    film_id: UUID,
    service: UgcService = Depends(),
):
    await service.delete_film_score(user_id=user_id, film_id=film_id)
    return Response(status_code=HTTP_204_NO_CONTENT)


@ugc_router.post("/bookmarks", response_model=BookmarkSchema, tags=["Bookmarks"])
async def add_bookmark(
    bookmark_data: CreateBookmarkSchema,
    service: UgcService = Depends(),
):
    return await service.add_bookmark(bookmark_data)


@ugc_router.get("/bookmarks/{user_id}", response_model=list[BookmarkSchema], tags=["Bookmarks"])
async def user_bookmarks(
    user_id: UUID,
    service: UgcService = Depends(),
):
    return await service.get_bookmarks(user_id=user_id)


@ugc_router.delete("/bookmarks/{user_id}/{film_id}", tags=["Bookmarks"])
async def delete_user_bookmark(
    user_id: UUID,
    film_id: UUID,
    service: UgcService = Depends(),
):
    await service.del_bookmark(user_id=user_id, film_id=film_id)
    return Response(status_code=HTTP_204_NO_CONTENT)


@ugc_router.post("/reviews", response_model=TextReviewSchema, tags=["Reviews"])
async def add_text_review(
    text_review_data: CreateTextReviewSchema,
    service: UgcService = Depends(),
):
    if review := await service.add_text_review(text_review_data):
        return JSONResponse(
            content=jsonable_encoder(review.model_dump()),
            status_code=HTTP_201_CREATED,
            headers={"Location": f"/reviews/{review.id}"},
        )
    raise HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail="Unable to create the review. Invalid data.",
    )


@ugc_router.get("/reviews/{film_id}", response_model=list[ReviewExtSchema], tags=["Reviews"])
async def get_text_review(
    film_id: UUID,
    service: UgcService = Depends(),
):
    return await service.get_film_reviews(film_id)


@ugc_router.put("/reviews/{review_id}/score", response_model=ScoreReviewSchema, tags=["Reviews"])
async def upsert_score_review(
    review_id: UUID,
    user_id: UUID,
    score: int = Query(..., ge=0, le=10),
    service: UgcService = Depends(),
):
    return await service.upsert_score_review(review_id, CreateScoreReviewSchema(user_id=user_id, score=score))
