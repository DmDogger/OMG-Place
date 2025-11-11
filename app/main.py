from fastapi import FastAPI
from httpx import Request
from starlette.responses import JSONResponse

from app.core.exceptions import ProductNotFound
from app.routers import categories, products, users, reviews
from fastapi_pagination import add_pagination
import time

from app.schemas import ResponseModel

app = FastAPI(
    title='OMG!Place',
    description='E-commerce API App.',
    version='0.1.0'
)


app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(reviews.router)

# Добавляем pagination в нашу аппку
add_pagination(app)

@app.get('/')
async def root():
    """
    Корневой маршрут
    """
    return {'message': 'Welcome to OMG!Place ecommerce app'}

