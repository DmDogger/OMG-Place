from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User as UserModel
from app.models.reviews import Review as ReviewModel

from app.core.exceptions import ReviewNotFound, ProductNotFound, SellerCannotLeaveReview, CanReviewOnlyOnce, \
    AccessDenied
from app.repositories.products_repo import ProductRepository
from app.repositories.review_repo import ReviewRepository
from app.schemas import ReviewCreate as ReviewCreateSchema
from app.services.product_service import ProductService


class ReviewService:
    def __init__(self,
                 review_repository: ReviewRepository ,
                 product_repository: ProductRepository,
                 product_service: ProductService
                 ):
        self._review_repository = review_repository
        self._product_repository = product_repository
        self._product_service = product_service

    async def get_reviews(self):
        """ Returns review list """
        return await self._review_repository.get_all()


    async def create_review(self, review_data: ReviewCreateSchema,
                            user: UserModel):
        """ Method allows a user to leave a review for a product """
        if user.role == 'seller':
            raise SellerCannotLeaveReview()
        product = await self._product_repository.get(review_data.product_id)
        if not product:
            raise ProductNotFound()
        if await self.user_already_reviewed_product(product.id, user.id):
            raise CanReviewOnlyOnce()
        review_data = review_data.model_dump()
        review_data.update({'user_id': user.id})
        review = await self._review_repository.create(review_data)
        await self._product_service.push_product_rating(product.id)
        await self._review_repository.db.commit() # Обратить внимание! Нужно переделать, чтобы транзакциями управлял не сервис!
        await self._review_repository.db.refresh(review)
        return review

    async def user_already_reviewed_product(self,
                                            product_id: int,
                                            user_id: int
                                            ) -> bool:
        """ Проверяет, оставлял ли пользователь отзыв или нет"""
        result = await self._review_repository.get_review_by_user(product_id, user_id)
        if result:
            return True
        return False

    async def delete_review(self, review_id: int,
                            user: UserModel):
        """ Method allows delete review by ID """
        if user.role != 'admin':
            raise AccessDenied()
        review = await self._review_repository.get(review_id)
        if not review:
            raise ReviewNotFound()
        product = await self._product_repository.get(review.product_id)
        if not product:
            raise ProductNotFound()
        await self._review_repository.delete(review_id)
        await self._review_repository.db.commit() # Обратить внимание! Нужно переделать, чтобы транзакциями управлял не сервис!
        await self._product_service.push_product_rating(product.id)
        await self._review_repository.db.commit() # Обратить внимание! Нужно переделать, чтобы транзакциями управлял не сервис!




