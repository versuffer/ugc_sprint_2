from uuid import UUID

from ugc_app.schemas.api.v1.schemas import ScoreSchema, BookmarkSchema, \
    CreateTextReviewSchema, TextReviewSchema, CreateBookmarkSchema, ReviewExtSchema, CreateScoreReviewSchema, \
    ScoreReviewSchema
from ugc_app.services.repositories.mongo.models import ScoreModel, BookmarkModel, TextReviewModel, ScoreReviewModel


class UgcService:

    async def get_score(self, film_id: UUID) -> ScoreSchema:
        scores = await ScoreModel.find(ScoreModel.film_id == str(film_id)).to_list()
        return ScoreSchema(film_id=UUID('79dadc3f-238f-451a-ad7f-042f2f23aa37'), user_id=UUID('2d51c501-c175-45aa-97cb-2c296cf32c32'), avg_score=9)

    async def add_score(self, user_id: UUID, film_id: UUID, score: int) -> ScoreSchema:
        score_document = {
            "user_id": str(user_id),
            "film_id": str(film_id),
            "score": score,
        }

        score = await ScoreModel(**score_document).insert()

        return await self.get_score(film_id)

    async def get_bookmarks(self, user_id: UUID) -> list[BookmarkSchema]:

        user_bookmarks = await BookmarkModel.find(BookmarkModel.user_id == user_id).to_list()

        return [BookmarkSchema.model_validate(bookmark.model_dump()) for bookmark in user_bookmarks]

    async def add_bookmark(self, bookmark_data: CreateBookmarkSchema) -> BookmarkSchema:

        user_bookmark = await BookmarkModel(**bookmark_data.model_dump()).insert()

        return BookmarkSchema.model_validate(user_bookmark.model_dump())

    async def del_bookmark(self, user_id: UUID, film_id: UUID) -> dict | None:
        if user_bookmark := await BookmarkModel.find_one(BookmarkModel.user_id == user_id, BookmarkModel.film_id == film_id):
            await user_bookmark.delete()
            return {"detail": "Bookmark successfully deleted"}
        return None

    async def add_text_review(self, text_review_data: CreateTextReviewSchema) -> TextReviewSchema:
        user_film_text_review = await TextReviewModel(**text_review_data.model_dump()).insert()
        return TextReviewSchema.model_validate(user_film_text_review.model_dump())

    async def add_score_review(self, review_id: UUID, score_review_data: CreateScoreReviewSchema) -> ScoreReviewSchema:
        update_data = score_review_data.model_dump() | {"review_id": review_id}

        review_score = await ScoreReviewModel.update_one({"review_id": review_id}, update_data, upsert=True)
        # review_score = await ScoreReviewModel(**score_review_data.model_dump() | {"review_id": review_id}).insert()
        return ScoreReviewSchema.model_validate(review_score.model_dump())

    async def get_film_reviews(self, film_id: UUID) -> list[ReviewExtSchema]:
        film_text_reviews = await TextReviewModel.find(TextReviewModel.film_id == film_id).to_list()
        return [ReviewExtSchema.model_validate(film_text_review.model_dump()) for film_text_review in film_text_reviews]
