import asyncio
import random
from uuid import uuid4
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from services.repositories.mongo.models import BookmarkModel, TextReviewModel, ScoreReviewModel, ScoreModel
from settings.config import settings


async def populate_db(num_records: int):
    client = AsyncIOMotorClient(settings.mongo_dsn)
    await init_beanie(database=client[settings.mongo_db], document_models=[BookmarkModel, TextReviewModel, ScoreReviewModel, ScoreModel])

    for _ in range(num_records):
        film_id = uuid4()
        user_id = uuid4()

        await BookmarkModel(film_id=film_id, user_id=user_id).insert()

        text_review = TextReviewModel(film_id=film_id, user_id=user_id, text="Sample review text", author="Author Name")
        await text_review.insert()

        score_review = ScoreReviewModel(user_id=user_id, review_id=text_review.id, score=random.randint(1, 10))
        await score_review.insert()

        score_model = ScoreModel(film_id=film_id, user_id=user_id, score=random.randint(1, 10))
        await score_model.insert()

        if (_ + 1) % 10000 == 0:
            print(f"Inserted {_ + 1} records")

async def main():
    await populate_db(10_000_000)

if __name__ == "__main__":
    asyncio.run(main())
