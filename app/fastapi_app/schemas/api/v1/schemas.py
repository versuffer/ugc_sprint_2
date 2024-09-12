import uuid

from pydantic import BaseModel

from app.fastapi_app.services.repositories.mongo.models import LikeModel


class MetricsSchemaIn(BaseModel):
    service_name: str
    metric_name: str
    metric_data: dict


class LikeSchema(BaseModel):
    likes: int
    dislikes: int

    @classmethod
    def from_model(cls, obj: LikeModel):
        return cls(likes=obj.likes, dislikes=obj.dislikes)


class ReviewSchema(BaseModel):  # TODO в тз больше требований
    film_id: uuid.UUID
    user_id: uuid.UUID
    text: str
    author: str


class BookmarkSchema(BaseModel):
    film_id: uuid.UUID
    user_id: uuid.UUID
