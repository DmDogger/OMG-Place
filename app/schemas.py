from pydantic import BaseModel, Field, ConfigDict, EmailStr
from decimal import Decimal
from datetime import datetime


# --- Модели Категорий ---
class CategoryCreate(BaseModel):
    """
    Модель для создания и обновления категорий.
    Используется в POST / PUT запросах
    (Это наша "Базовая" модель)
    """
    name: str = Field(
        min_length=3,
        max_length=50,
        description='Название категории (3-50 символов)')

    parent_id: int | None = Field(
        default=None,
        description='ID родительской категории (если имеется)'
    )


class Category(CategoryCreate):
    """
    Модель для ответа с данными категории.
    Используется в GET запросах
    """
    id: int = Field(description='Уникальный ID категории')
    is_active: bool = Field(description='Активность категории')

    model_config = ConfigDict(from_attributes=True)


# --- Модели Товаров ---
class ProductCreate(BaseModel):
    """
    Модель для создания и обновления категорий.
    Используется в POST / PUT запросах
    """
    name: str = Field(
        min_length=3,
        max_length=100,
        description='Название товара (3-100 символов)'
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        description='Поле для описания товара (до 500 символов)'
    )
    price: Decimal = Field(
        gt=0,
        description='Цена товара (больше 0 у.е)',
        decimal_places=2)
    image_url: str | None = Field(
        default=None,
        max_length=200,
        description='URL изображения товара'
    )
    stock: int = Field(
        ge=0,
        description='Количество товара на складе (0 или больше)'
    )
    category_id: int = Field(
        gt=0,
        description='ID категории товара'
    )


class Product(ProductCreate):
    """
    Модель для ответа с данными товара.
    Используется в GET запросах
    """
    is_active: bool = Field(description='Активность товара')
    model_config = ConfigDict(from_attributes=True)
    rating: float

class UserCreate(BaseModel):
    """
    Модель для создания пользователей.
    Используется в POST запросах
    """
    email: EmailStr = Field(description='Email пользователя')
    password: str = Field(min_length=8, description='Пароль пользователя (не менее 8 символов)')
    role: str = Field(default='buyer', pattern='^(buyer|seller|admin)$', description='Роль: "buyer" / "seller" / "admin"')


class User(BaseModel):
    """
    Модель для ответа.
    Содержит данные пользователя.
    Используется в GET-запросах
    """
    id: int
    email: str
    is_active: bool
    role: str
    model_config = ConfigDict(from_attributes=True)

class ReviewCreate(BaseModel):
    """
    Модель для создания и обновления отзывов.
    Используется в POST / PUT запросах.
    """
    product_id: int
    comment: str | None = Field(
                         min_length=10,
                         max_length=500,
                         default=None,
                         description='Отзыв на товар (максимум 500 символов)'
                         )
    grade: int = Field(ge=1, le=5, description='Оценка товара. От 1 до 5.')


class Review(BaseModel):
    """ Модель для ответа.
    Содержит данные об отзыве.
    Используется в GET - запросах"""
    id: int = Field(description='Уникальный ID отзыва')
    user_id: int
    product_id: int
    comment: str | None = Field(default=None)
    comment_date: datetime
    is_active: bool
    grade: int

