from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User as UserModel
from app.models.reviews import Review as ReviewModel

from app.core.exceptions import ReviewNotFound

async def find_active_review(review_id: int,
                             db: AsyncSession):
    """ Метод находит активный отзыв и возвращает его """
    review = await db.scalars(select(ReviewModel).where(ReviewModel.id == review_id,
                                                  ReviewModel.is_active == True))
    if not review.first():
        raise ReviewNotFound()
    return review

async def get_user_active_review(review_id: int,
                                 current_user: UserModel,
                                 db: AsyncSession) -> ReviewModel:
    """ Возвращает активный отзыв пользователя если он существует """
    review = await db.scalars(select(ReviewModel).where(ReviewModel.user_id == current_user.id,
                                                        ReviewModel.id == review_id,
                                         ReviewModel.is_active == True))
    review = review.first()
    if not review:
        raise ReviewNotFound()
    return review

async def user_already_reviewed_product(product_id: int,
                                        user_id: int,
                                        db: AsyncSession) -> bool:
    """ Проверяет, оставлял ли пользователь отзыв или нет"""
    result = await db.scalars(select(ReviewModel).where(ReviewModel.product_id == product_id,
                                                        ReviewModel.user_id == user_id,
                                                        ReviewModel.is_active == True))
    if result.first():
        return True
    return False
