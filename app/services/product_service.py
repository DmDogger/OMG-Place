from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.products import Product as ProductModel
from app.models.users import User as UserModel
from app.models.reviews import Review as ReviewModel
from fastapi import HTTPException

from app.services import find_category
from app.core.exceptions import ProductNotFound, CategoryNotFound


async def validate_product_ownership(product_id: int,
                                     current_user: UserModel,
                                     db: AsyncSession):
    """ Подтверждает связь владельца продукта с продуктом """
    res = await db.scalars(select(ProductModel).where(ProductModel.seller_id == current_user.id,
                                                      ProductModel.id == product_id,
                                                      ProductModel.is_active == True))
    return res.first()

async def find_all_active_products(db: AsyncSession):
    """ Находит все активные товары """
    stmt = select(ProductModel).where(ProductModel.is_active == True)
    res = await db.scalars(stmt)
    return res.all()

async def find_active_product(product_id: int, db: AsyncSession):
    """ Находит активный товар """
    cursor = await db.scalars(select(ProductModel).where(ProductModel.id == product_id,
                                                         ProductModel.is_active == True))
    return cursor.first()

async def calculate_avg_rating(product_id: int,
                        db: AsyncSession):
    """ Метод для расчета среднего рейтинга продукта"""
    # --- Сначала найдем продукт ---
    product = await find_active_product(product_id, db)
    if not product:
        raise ProductNotFound()
    # ---- Потом проверим существование категории --
    category = await find_category(product.category_id, db)
    if not category:
        raise CategoryNotFound()
    # --- Формируем рейтинг ---
    reviews = await db.scalars(select(ReviewModel).where(ReviewModel.product_id == product_id,
                                                   ReviewModel.is_active == True))
    reviews = reviews.all()
    if not reviews:
        return 0.0

    total = sum(rev.grade for rev in reviews)
    avg = total / len(reviews)
    return avg

async def push_product_rating(product_id,
                              db: AsyncSession):
    new_rating = await calculate_avg_rating(product_id, db)
    await db.execute(
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(rating=new_rating)
    )
    await db.commit()








