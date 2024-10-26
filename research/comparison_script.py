import asyncio
import time

import asyncpg
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from services.repositories.mongo.models import BookmarkModel, ScoreModel
from settings.config import settings

DATABASE_URL = "postgresql://postgres:postgres@localhost/movies_db"


async def fetch_pg_user_ids(conn):
    users = await conn.fetch("SELECT DISTINCT user_id FROM film_scores LIMIT 100")
    return [user['user_id'] for user in users]


async def fetch_mongo_user_ids():
    scores = await ScoreModel.find().to_list(length=100)
    return list({score.user_id for score in scores})


async def fetch_pg_film_ids(conn):
    films = await conn.fetch("SELECT DISTINCT film_id FROM film_scores LIMIT 100")
    return [film['film_id'] for film in films]


async def fetch_mongo_film_ids():
    scores = await ScoreModel.find().to_list(length=100)
    return list({score.film_id for score in scores})


async def pg_count_user_likes(conn, user_id):
    return await conn.fetchval("SELECT COUNT(*) FROM film_scores WHERE user_id = $1", user_id)


async def mongo_count_user_likes(user_id):
    return await ScoreModel.find(ScoreModel.user_id == user_id).count()


async def pg_count_user_bookmarks(conn, user_id):
    return await conn.fetchval("SELECT COUNT(*) FROM bookmarks WHERE user_id = $1", user_id)


async def mongo_count_user_bookmarks(user_id):
    return await BookmarkModel.find(BookmarkModel.user_id == user_id).count()


async def avg_score_pg(film_id, conn):
    return await conn.fetchval("SELECT AVG(score) FROM film_scores WHERE film_id = $1", film_id)


async def avg_score_mongo(film_id):
    return await ScoreModel.find(ScoreModel.film_id == film_id).avg("score")


async def compare_performance():
    # Подключение к PostgreSQL
    pg_conn = await asyncpg.connect(DATABASE_URL)
    # Подключение к MongoDB
    mongo_client = AsyncIOMotorClient(settings.mongo_dsn)
    await init_beanie(database=mongo_client[settings.mongo_db], document_models=[BookmarkModel, ScoreModel])

    # Получение уникальных user_ids и film_ids
    pg_user_ids = await fetch_pg_user_ids(pg_conn)
    mongo_user_ids = await fetch_mongo_user_ids()
    pg_film_ids = await fetch_pg_film_ids(pg_conn)
    mongo_film_ids = await fetch_mongo_film_ids()

    # Сбор результатов для записи
    results = []

    # Инициализация для анализа общей производительности
    total_pg_duration = 0
    total_mongo_duration = 0
    total_pg_likes = 0
    total_mongo_likes = 0

    # Инициализация для средних временных показателей
    pg_likes_duration = 0
    mongo_likes_duration = 0
    pg_bookmarks_duration = 0
    mongo_bookmarks_duration = 0
    pg_avg_score_duration = 0
    mongo_avg_score_duration = 0

    # Сравнение запросов
    for user_id in pg_user_ids:
        # PostgreSQL
        start_time = time.time()
        likes_pg = await pg_count_user_likes(pg_conn, user_id)
        pg_likes_duration += time.time() - start_time

        start_time = time.time()
        bookmarks_pg = await pg_count_user_bookmarks(pg_conn, user_id)
        pg_bookmarks_duration += time.time() - start_time

        total_pg_duration += pg_likes_duration + pg_bookmarks_duration
        total_pg_likes += likes_pg

        results.append(
            f"[PostgreSQL] User: {user_id}, Likes: {likes_pg}, Bookmarks: {bookmarks_pg}, "
            f"Total Duration: {total_pg_duration:.4f}s"
        )

    for user_id in mongo_user_ids:
        # MongoDB
        start_time = time.time()
        likes_mongo = await mongo_count_user_likes(user_id)
        mongo_likes_duration += time.time() - start_time

        start_time = time.time()
        bookmarks_mongo = await mongo_count_user_bookmarks(user_id)
        mongo_bookmarks_duration += time.time() - start_time

        total_mongo_duration += mongo_likes_duration + mongo_bookmarks_duration
        total_mongo_likes += likes_mongo

        results.append(
            f"[MongoDB] User: {user_id}, Likes: {likes_mongo}, Bookmarks: {bookmarks_mongo}, "
            f"Total Duration: {total_mongo_duration:.4f}s"
        )

    # Сравнение средних оценок фильмов
    for film_id in pg_film_ids:
        # PostgreSQL
        start_time = time.time()
        avg_pg = await avg_score_pg(film_id, pg_conn)
        pg_avg_score_duration += time.time() - start_time

        results.append(f"[Film ID: {film_id}] Avg PG: {avg_pg}, Duration: {pg_avg_score_duration:.4f}s")

    for film_id in mongo_film_ids:
        # MongoDB
        start_time = time.time()
        avg_mongo = await avg_score_mongo(film_id)
        mongo_avg_score_duration += time.time() - start_time

        results.append(f"[Film ID: {film_id}] Avg Mongo: {avg_mongo}, Duration: {mongo_avg_score_duration:.4f}s")

    await pg_conn.close()

    # Запись результатов в файл
    with open("performance_comparison_report.txt", "w") as f:
        f.write("Performance Comparison Report\n")
        f.write("=" * 40 + "\n")
        for result in results:
            f.write(result + "\n")

        # Вывод общего резюме
        f.write("\nSummary of Performance Comparison:\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total likes in PostgreSQL: {total_pg_likes}\n")
        f.write(f"Total duration in PostgreSQL: {total_pg_duration:.4f}s\n")
        f.write(f"Total likes in MongoDB: {total_mongo_likes}\n")
        f.write(f"Total duration in MongoDB: {total_mongo_duration:.4f}s\n")

        # Среднее время для каждого типа запроса
        avg_pg_likes_time = pg_likes_duration / len(pg_user_ids) if pg_user_ids else 0
        avg_pg_bookmarks_time = pg_bookmarks_duration / len(pg_user_ids) if pg_user_ids else 0
        avg_mongo_likes_time = mongo_likes_duration / len(mongo_user_ids) if mongo_user_ids else 0
        avg_mongo_bookmarks_time = mongo_bookmarks_duration / len(mongo_user_ids) if mongo_user_ids else 0

        f.write("\nAverage Time for Each Query:\n")
        f.write("=" * 40 + "\n")
        f.write(f"Average time for likes in PostgreSQL: {avg_pg_likes_time:.4f}s\n")
        f.write(f"Average time for bookmarks in PostgreSQL: {avg_pg_bookmarks_time:.4f}s\n")
        f.write(f"Average time for likes in MongoDB: {avg_mongo_likes_time:.4f}s\n")
        f.write(f"Average time for bookmarks in MongoDB: {avg_mongo_bookmarks_time:.4f}s\n")


if __name__ == "__main__":
    asyncio.run(compare_performance())
