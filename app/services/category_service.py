from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.categories import Category as CategoryModel

async def find_all_active_categories(db: AsyncSession):
    """ Находит все активные категории """
    cursor = await db.scalars(select(CategoryModel).where(CategoryModel.is_active == True))
    return cursor.all()


async def find_category(category_id, db: AsyncSession):
    """ Находит активную категорию"""
    cursor = await db.scalars(select(CategoryModel).where(CategoryModel.id == category_id,
                                                    CategoryModel.is_active == True))
    return cursor.first()
