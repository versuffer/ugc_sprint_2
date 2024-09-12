import uuid

from app.fastapi_app.schemas.api.v1.schemas import LikeSchema, ReviewSchema, BookmarkSchema


class UgcService:
    def add_likes(self, film_id: uuid.UUID) -> list[LikeSchema]:
        return [
            LikeSchema(
                film_id='79dadc3f-238f-451a-ad7f-042f2f23aa37',
                user_id='2d51c501-c175-45aa-97cb-2c296cf32c32',
                score=9
            )
        ]

    def get_likes(self, film_id: uuid.UUID) -> list[LikeSchema]:
        return [
            LikeSchema(
                film_id='79dadc3f-238f-451a-ad7f-042f2f23aa37',
                user_id='2d51c501-c175-45aa-97cb-2c296cf32c32',
                score=9
            )
        ]

    def get_reviews(self, film_id: uuid.UUID) -> list[ReviewSchema]:
        return [
            ReviewSchema(
                film_id='79dadc3f-238f-451a-ad7f-042f2f23aa37',
                user_id='2d51c501-c175-45aa-97cb-2c296cf32c32',
                text='очень хороший фильм',
                author='барабас',
            )
        ]

    def get_bookmarks(self, film_id: uuid.UUID) -> list[BookmarkSchema]:
        return [
            BookmarkSchema(
                film_id='79dadc3f-238f-451a-ad7f-042f2f23aa37',
                user_id='2d51c501-c175-45aa-97cb-2c296cf32c32',
            )
        ]
