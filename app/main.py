from fastapi import FastAPI, Request
from app.routers import categories, products, users, reviews
from fastapi.responses import JSONResponse
app = FastAPI(
    title='FastAPI Ecommerce app',
    version='0.1.0'
)


# Подключаем маршруты к main.py (из routers)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(reviews.router)

@app.get('/')
async def root():
    """
    Корневой маршрут
    """
    return {'message': 'Welcome to fastAPI ecommerce app'}

