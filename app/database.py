from sqlalchemy import create_engine, String, Integer, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

# Строка подключения к БД
DATABASE_URL = "sqlite:///ecommerce.db"

# Создаем Engine
engine = create_engine(DATABASE_URL, echo=True)

# Фабрика сеансов
SessionLocal = sessionmaker(bind=engine)

# Базовый класс для моделей
class Base(DeclarativeBase):
    pass

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Строка подключения для PostgreSQl
DATABASE_URL = "postgresql+asyncpg://ecommerce_user:ecommerce_12345@localhost:5432/ecommerce_db"

# Создаём Engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


