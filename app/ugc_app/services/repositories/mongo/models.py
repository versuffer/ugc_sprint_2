from datetime import datetime, timezone
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field


class BaseDocument(Document):
    id: UUID = Field(default_factory=uuid4)
    film_id: UUID
    user_id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BookmarkModel(BaseDocument):
    pass


class TextReviewModel(BaseDocument):
    text: str
    author: str


class ScoreReviewModel(Document):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    review_id: UUID
    score: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ScoreModel(BaseDocument):
    score: int
