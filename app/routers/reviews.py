from fastapi import APIRouter, Depends

from app.core.dependecies.services.review_service import get_review_service

from app.auth import get_current_user, get_current_admin
from app.schemas import ReviewCreate as ReviewCreateSchema, Review as ReviewSchema
from app.models.users import User as UserModel
from app.services.review_service import ReviewService

router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)

@router.get('/', status_code=200)
async def get_all_reviews(review_service: ReviewService = Depends(get_review_service)):
    """ Return list of reviews """
    return await review_service.get_reviews()

@router.post('/', response_model=ReviewSchema, status_code=201)
async def create_review(review_data: ReviewCreateSchema,
                        review_service: ReviewService = Depends(get_review_service),
                        user: UserModel = Depends(get_current_user)):
    return await review_service.create_review(review_data, user)

@router.delete('/{review_id}', status_code=200)
async def delete_review(review_id: int,
                        user: UserModel = Depends(get_current_admin),
                        review_service: ReviewService = Depends(get_review_service)):
    await review_service.delete_review(review_id, user)
    return {'message': f'review with id {review_id} was deleted successfully'}









