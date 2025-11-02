from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ProductNotFound, CategoryNotFound, SellerCannotLeaveReview, CanReviewOnlyOnce, ReviewNotFound

from app.auth import get_current_user, get_current_admin

from app.schemas import ReviewCreate as ReviewCreateSchema, Review as ReviewSchema
from app.models.reviews import Review as ReviewModel
from app.models.users import User as UserModel

from app.services import  find_active_product, find_active_review, user_already_reviewed_product, push_product_rating
from app.db_depends import get_async_db

router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)

@router.get('/', status_code=200)
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """ Возвращает список всех отзывов """
    reviews = await db.scalars(select(ReviewModel))
    return reviews.all()


@router.post('/', response_model=ReviewSchema, status_code=201)
async def create_review(review_data: ReviewCreateSchema,
                        current_user: UserModel = Depends(get_current_user),
                        db: AsyncSession = Depends(get_async_db)):
    """ Метод позволяет добавить отзыв """
    product = await find_active_product(review_data.product_id, db)
    if not product:
        raise ProductNotFound()
    if current_user.role == 'seller':
        raise SellerCannotLeaveReview()
    if await user_already_reviewed_product(review_data.product_id, current_user.id, db):
        raise CanReviewOnlyOnce()

    review = ReviewModel(user_id=current_user.id,
                         product_id=review_data.product_id,
                         grade=review_data.grade,
                         comment=review_data.comment)

    db.add(review)
    await db.commit()
    await db.refresh(review)
    await push_product_rating(product.id, db)
    return review

@router.delete('/{review_id}', status_code=200)
async def delete_review(review_id: int,
                        current_user_admin: UserModel = Depends(get_current_admin),
                        db: AsyncSession = Depends(get_async_db)):
    """ Метод позволяет удалить отзыв """
    review = await find_active_review(review_id, db)
    if not review:
        raise ReviewNotFound()
    product = await find_active_product(review.product_id, db)
    if not product:
        raise ProductNotFound()

    review.is_active=False

    await db.commit()
    await db.refresh(review)
    await push_product_rating(product.id, db)
    return {"message": f"review with ID: {review_id} was deleted successfully"}










