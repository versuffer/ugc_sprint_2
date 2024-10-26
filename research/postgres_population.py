import asyncio
import random
import time
from datetime import UTC, datetime
from uuid import UUID, uuid4

import asyncpg
import sqlalchemy as sa
from sqlmodel import Field, SQLModel, create_engine

DATABASE_URL = "postgresql://postgres:postgres@localhost/movies_db"
engine = create_engine(DATABASE_URL, echo=True)


class BookmarkModel(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True)
    film_id: str
    user_id: str
    created_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False))

    __tablename__ = 'bookmarks'


class TextReviewModel(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True)
    film_id: str
    user_id: str
    text: str
    author: str
    created_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False))

    __tablename__ = 'review_texts'


class ScoreReviewModel(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True)
    user_id: str
    review_id: str
    score: int

    __tablename__ = 'review_scores'


class ScoreModel(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True)
    film_id: str
    user_id: str
    score: int
    created_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False))

    __tablename__ = 'film_scores'


def create_tables():
    SQLModel.metadata.create_all(engine)


async def populate_db(num_records: int):
    start_time = time.time()
    conn = await asyncpg.connect(DATABASE_URL)

    film_ids = [str(uuid4()) for _ in range(500)]
    user_ids = [str(uuid4()) for _ in range(10000)]

    for _ in range(num_records):
        id_ = str(uuid4())
        film_id = random.choice(film_ids)
        user_id = random.choice(user_ids)

        await conn.execute(
            'INSERT INTO bookmarks (id, film_id, user_id, created_at) VALUES ($1, $2, $3, $4)',
            id_,
            film_id,
            user_id,
            datetime.now(UTC),
        )

        id_ = str(uuid4())
        text_review_query = await conn.fetchrow(
            'INSERT INTO review_texts (id, film_id, user_id, text, author, created_at) VALUES '
            '($1, $2, $3, $4, $5, $6) RETURNING id',
            id_,
            film_id,
            user_id,
            "Sample review text",
            "Author Name",
            datetime.now(UTC),
        )

        review_id = str(text_review_query['id'])

        id_ = str(uuid4())
        await conn.execute(
            'INSERT INTO review_scores (id, user_id, review_id, score) VALUES ($1, $2, $3, $4)',
            id_,
            user_id,
            review_id,
            random.randint(1, 10),
        )

        id_ = str(uuid4())
        await conn.execute(
            'INSERT INTO film_scores (id, film_id, user_id, score, created_at) VALUES ($1, $2, $3, $4, $5)',
            id_,
            film_id,
            user_id,
            random.randint(1, 10),
            datetime.now(UTC),
        )

        if (_ + 1) % 10000 == 0:
            print(f"Inserted {_ + 1} records")

    await conn.close()
    end_time = time.time()
    print(f"Время вставки {num_records} записей: {end_time - start_time:.2f} секунд")


async def main():
    create_tables()
    await populate_db(200_000)


if __name__ == "__main__":
    asyncio.run(main())
