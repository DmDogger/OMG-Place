from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_seller
from app.models.products import Product as ProductModel
from app.models.users import User as UserModel
from app.schemas import ProductCreate as ProductCreateSchema, Product as ProductSchema
from app.services import find_all_active_products, find_active_product, find_category, validate_product_ownership
from app.core.exceptions import CategoryNotFound, ProductNotFound, ProductOwnershipError

from app.db_depends import get_async_db
router = APIRouter(
    prefix='/products',
    tags=['products']
)

@router.get('/', response_model=list[ProductSchema], status_code=200)
async def get_all_active_products(db: AsyncSession = Depends(get_async_db)):
    products = await find_all_active_products(db)
    return products


@router.post('/',response_model=ProductSchema, status_code=201)
async def create_product(product: ProductCreateSchema,
                         current_user: UserModel = Depends(get_current_seller),
                         db: AsyncSession = Depends(get_async_db)):
    """ Добавить товар. (Только для селлеров)"""
    # проверка существования категории
    category = await find_category(product.category_id, db)
    if category is None:
        raise CategoryNotFound()

    new_product_orm = ProductModel(**product.model_dump(),
                                   seller_id=current_user.id)

    db.add(new_product_orm)
    await db.commit()
    await db.refresh(new_product_orm)

    return new_product_orm


@router.get('/{category_id}', response_model=list[ProductSchema])
async def get_products_by_category(category_id: int,
                                   db: AsyncSession = Depends(get_async_db)):
    """ Возвращает товар в категории по его ID """
    # существует ли категория?
    category = await find_category(category_id, db)
    if category is None:
        raise CategoryNotFound()
    # есть ли продукты в этой категории?
    products = await find_active_product(category_id, db)
    if not products:
        raise ProductNotFound()
    return products


@router.get("/{product_id}", response_model=ProductSchema) ###### refactoring --->
async def get_product(product_id: int,
                      db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает детальную информацию о товаре по его ID.
    """
    # есть ли активный товар с таким ид
    product_data = await find_active_product(product_id, db)
    if product_data is None:
        raise ProductNotFound()
    # проверяем есть существует категория с этим продуктом
    category = await find_category(product_data.category_id, db)
    if category is None:
        raise CategoryNotFound()
    return product_data

@router.delete("/{product_id}", status_code=200)
async def delete_product(product_id: int,
                         current_user: UserModel = Depends(get_current_seller),
                         db: AsyncSession = Depends(get_async_db)):
    """
    Удаляет продукт по его ID.
    """
    # --- Проверка существования продукта ---
    product = await find_active_product(product_id, db)
    if not product:
        raise ProductNotFound()

    # --- Проверка привязки товара к продавцу --
    if not await validate_product_ownership(product_id, current_user, db):
        raise ProductOwnershipError()
    # --- Мягкое удаление продукта
    product.is_active = False
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return {"status": "success", "message": "product marked as inactive"}

@router.put('/{product_id}', response_model=ProductSchema, status_code=200)
async def update_product(product_id: int,
                         product_data: ProductCreateSchema,
                         current_user = Depends(get_current_seller),
                         db: AsyncSession = Depends(get_async_db)):
    """ Обновить данные товара (Только admin или seller)"""
    # --- Проверяем существование товара ---
    product = await find_active_product(product_id, db)
    if not product:
        raise ProductNotFound()
    # --- Проверяем привязку товара (если роль - seller) ---
    if not await validate_product_ownership(product_id, current_user, db):
        raise ProductOwnershipError()
    # --- Проверяем существование категории ---
    category = await find_category(product_data.category_id, db)
    if not category:
        raise CategoryNotFound()
    # --- Обновляем данные ---
    update_data = product_data.model_dump()
    for key, value in update_data.items():
        setattr(product, key, value)
    # --- Работаем с базой данных ---
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product





