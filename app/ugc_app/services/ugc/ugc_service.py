from uuid import UUID

from ugc_app.schemas.api.v1.schemas import (
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
from ugc_app.services.repositories.mongo.models import (
    BookmarkModel,
    ScoreModel,
    ScoreReviewModel,
    TextReviewModel,
)


class UgcService:

    @staticmethod
    async def get_score(film_id: UUID) -> ScoreSchema:
        avg_score = await ScoreModel.find(ScoreModel.film_id == film_id).avg(ScoreModel.score)

        return ScoreSchema(film_id=film_id, avg_score=avg_score)

    @staticmethod
    async def upsert_score(user_id: UUID, film_id: UUID, score: int) -> CreateScoreSchema:
        upsert_document = {
            "user_id": user_id,
            "film_id": film_id,
            "score": score,
        }

        if user_film_score := await ScoreModel.find_one(ScoreModel.film_id == film_id, ScoreModel.user_id == user_id):
            await user_film_score.set(upsert_document)
            return CreateScoreSchema.model_validate(user_film_score.model_dump())

        user_film_score = await ScoreModel(**upsert_document).insert()
        return CreateScoreSchema.model_validate(user_film_score.model_dump())

    @staticmethod
    async def delete_film_score(user_id: UUID, film_id: UUID) -> str | None:
        if user_film_score := await ScoreModel.find_one(ScoreModel.film_id == film_id, ScoreModel.user_id == user_id):
            await user_film_score.delete()
        return None

    @staticmethod
    async def get_bookmarks(user_id: UUID) -> list[BookmarkSchema]:

        user_bookmarks = await BookmarkModel.find(BookmarkModel.user_id == user_id).to_list()

        return [BookmarkSchema.model_validate(bookmark.model_dump()) for bookmark in user_bookmarks]

    @staticmethod
    async def add_bookmark(bookmark_data: CreateBookmarkSchema) -> BookmarkSchema:

        user_bookmark = await BookmarkModel(**bookmark_data.model_dump()).insert()

        return BookmarkSchema.model_validate(user_bookmark.model_dump())

    @staticmethod
    async def del_bookmark(user_id: UUID, film_id: UUID) -> dict | None:
        if user_bookmark := await BookmarkModel.find_one(
            BookmarkModel.user_id == user_id, BookmarkModel.film_id == film_id
        ):
            await user_bookmark.delete()
            return {"detail": "Bookmark successfully deleted"}
        return None

    @staticmethod
    async def add_text_review(
        text_review_data: CreateTextReviewSchema,
    ) -> TextReviewSchema:
        user_film_text_review = await TextReviewModel(**text_review_data.model_dump()).insert()
        return TextReviewSchema.model_validate(user_film_text_review.model_dump())

    @staticmethod
    async def upsert_score_review(review_id: UUID, score_review_data: CreateScoreReviewSchema) -> ScoreReviewSchema:
        upsert_data = score_review_data.model_dump() | {"review_id": review_id}

        if review_score := await ScoreReviewModel.find_one(ScoreReviewModel.review_id == review_id):
            await review_score.set(upsert_data)
            return ScoreReviewSchema.model_validate(review_score.model_dump())

        review_score = await ScoreReviewModel(**upsert_data).insert()
        return ScoreReviewSchema.model_validate(review_score.model_dump())

    @staticmethod
    async def get_film_reviews(film_id: UUID) -> list[ReviewExtSchema]:
        film_text_reviews = await TextReviewModel.find(TextReviewModel.film_id == film_id).to_list()
        return [ReviewExtSchema.model_validate(film_text_review.model_dump()) for film_text_review in film_text_reviews]
