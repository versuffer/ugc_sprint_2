import asyncio
import random
from uuid import uuid4
import time

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from services.repositories.mongo.models import (
    BookmarkModel,
    ScoreModel,
    ScoreReviewModel,
    TextReviewModel,
)
from settings.config import settings


async def populate_db(num_records: int):
    start_time = time.time()
    client = AsyncIOMotorClient(settings.mongo_dsn)
    await init_beanie(
        database=client[settings.mongo_db],
        document_models=[BookmarkModel, TextReviewModel, ScoreReviewModel, ScoreModel],
    )

    film_ids = [str(uuid4()) for _ in range(500)]
    user_ids = [str(uuid4()) for _ in range(10000)]

    for _ in range(num_records):
        film_id = random.choice(film_ids)
        user_id = random.choice(user_ids)

        await BookmarkModel(film_id=film_id, user_id=user_id).insert()

        text_review = TextReviewModel(film_id=film_id, user_id=user_id, text="Sample review text", author="Author Name")
        await text_review.insert()

        score_review = ScoreReviewModel(user_id=user_id, review_id=text_review.id, score=random.randint(1, 10))
        await score_review.insert()

        score_model = ScoreModel(film_id=film_id, user_id=user_id, score=random.randint(1, 10))
        await score_model.insert()

        if (_ + 1) % 10000 == 0:
            print(f"Inserted {_ + 1} records")

    end_time = time.time()
    print(f"Время вставки {num_records} записей: {end_time - start_time:.2f} секунд")


async def main():
    await populate_db(200_000)


if __name__ == "__main__":
    asyncio.run(main())
