import uuid
from datetime import datetime, timezone
from beanie import Document
from pydantic import Field, BaseModel


class Bookmark(Document):
    film_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LikeModel(BaseModel):
    id: uuid.UUID
    film_id: uuid.UUID
    user_id: uuid.UUID
    rating: int

    @staticmethod
    def get_min_rating():
        return 0

    @staticmethod
    def get_max_rating():
        return 10

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
