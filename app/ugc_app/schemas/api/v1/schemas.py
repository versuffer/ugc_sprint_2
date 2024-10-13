from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ScoreSchema(BaseModel):
    film_id: UUID
    avg_score: float


class CreateScoreSchema(BaseModel):
    film_id: UUID
    user_id: UUID
    score: int


class CreateTextReviewSchema(BaseModel):
    film_id: UUID
    user_id: UUID
    text: str
    author: str


class CreateScoreReviewSchema(BaseModel):
    user_id: UUID
    score: int


class TextReviewSchema(BaseModel):
    id: UUID
    film_id: UUID
    user_id: UUID
    text: str
    author: str
    created_at: datetime


class ScoreReviewSchema(CreateScoreReviewSchema):
    id: UUID
    review_id: UUID
    created_at: datetime

    class Config:
        fields = {
            "id": "id",
            "review_id": "review_id",
            "user_id": "user_id",
            "score": "score",
            "created_at": "created_at",
        }


class ReviewExtSchema(BaseModel):
    id: UUID
    film_id: UUID
    user_id: UUID
    text: str
    author: str
    author_score: int = 10
    created_at: datetime


class CreateBookmarkSchema(BaseModel):
    film_id: UUID
    user_id: UUID


class BookmarkSchema(BaseModel):
    id: UUID
    film_id: UUID
    user_id: UUID
    created_at: datetime
