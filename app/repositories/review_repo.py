from app.repositories.base_repo import BaseSQLRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sql_update
from app.database import Base
from app.models.reviews import Review as ReviewModel

# Repository for reviews works with ORM-models

class ReviewRepository(BaseSQLRepository):
    def __init__(self, db: AsyncSession, model: Base):
        super().__init__(db, model)

    async def get(self, id_: int):
        stmt = select(ReviewModel).where(ReviewModel.id == id_,
                                         ReviewModel.is_active == True)
        return await self.db.scalar(stmt)

    async def get_all(self):
        stmt = select(ReviewModel).where(ReviewModel.is_active == True)
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_reviews_by_product_id(self, id_: int):
        stmt = select(ReviewModel).where(ReviewModel.product_id == id_,
                                         ReviewModel.is_active == True)
        result = await self.db.scalars(stmt)
        result = result.all()
        return result

    async def get_review_by_user(self,
                                 product_id: int,
                                 user_id: int):
        stmt = select(ReviewModel).where(ReviewModel.product_id == product_id,
                                         ReviewModel.user_id == user_id,
                                         ReviewModel.is_active == True)
        result = await self.db.scalars(stmt)
        return result.first()

    async def create(self, review: dict):
        review = ReviewModel(**review)
        self.db.add(review)
        return review


    async def update(self, id_: int, updated_data: dict):
        stmt = (
            sql_update(ReviewModel)
            .where(ReviewModel.id == id_,
                       ReviewModel.is_active == True)
            .values(**updated_data)
        )
        await self.db.execute(stmt)
        return self.get(id_)

    async def delete(self, id_):
        stmt = select(ReviewModel).where(ReviewModel.id == id_,
                                         ReviewModel.is_active == True)
        review = await self.db.scalar(stmt)
        if not review:
            return None
        review.is_active = False
        self.db.add(review)
        return review


