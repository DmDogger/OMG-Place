from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

from app.models.users import User as UserModel
from app.schemas import UserCreate, User as UserSchema
from app.db_depends import get_async_db
from app.auth import hash_password, verify_password, create_access_token, get_current_user, get_current_admin,  create_refresh_token, \
    oauth2_scheme
from app.config import SECRET_KEY, ALGORITHM

import jwt

router = APIRouter(prefix='/users',
                   tags=['users'])

@router.get('/me', response_model=UserSchema, status_code=200)
async def get_current_user(current_user: UserModel = Depends(get_current_user),
                           db: AsyncSession = Depends(get_async_db)):
    return current_user


@router.post('/', response_model=UserSchema, status_code=201)
async def create_user(user: UserCreate,
                      db: AsyncSession = Depends(get_async_db)):
    """
    Создает нового пользователя.
    """
    # --- Уникальный ли E-mail? ---
    email = await db.scalars((select(UserModel).where(UserModel.email == user.email)))
    if email.first():
        raise HTTPException(status_code=409, detail='Email already registered')

    # --- Создаем ORM пользователя с хеш-паролем ---
    new_user = UserModel(email=user.email,
                         hashed_password=hash_password(user.password),
                         role=user.role)
    # --- Работаем с DB ---
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post('/token', status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_async_db)):
    # --- Проверка существования пользователя ---
    user = await db.scalars(select(UserModel).where(UserModel.email == form_data.username,
                                                    UserModel.is_active == True))
    user = user.first()
    if not user:
        raise HTTPException(status_code=400,
                            detail='User with this login not exist',
                            headers={'WWW-Authentication':'Bearer'})
    # --- Проверка правильности введенного пароля ---
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400,
                            detail='Not correct user or password',
                            headers={'WWW-Authentication': 'Bearer'})
    # --- Создаем JWT (access) ---
    access_token = create_access_token(data={'sub': user.email,
                                        'role': user.role,
                                             'id': user.id})
    # --- Создаем JWT (refresh) ---
    refresh_token = create_refresh_token(data={'sub': user.email,
                                        'role': user.role,
                                             'id': user.id})
    return {'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer'}

@router.post('/refresh-token', status_code=200)
async def refresh_token(refresh_token: str = Depends(oauth2_scheme),
                        db: AsyncSession = Depends(get_async_db)):
    """ Обновляет access-token с помощью refresh-token """
    credentials_exception = HTTPException(status_code=401,
                                          detail='Could not validate refresh token',
                                          headers={'WWW-Authenticate': 'Bearer'})
    # --- Проверка refresh-token ---
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithm=ALGORITHM)
        email: str = payload.get('sub')
        if not email:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    # --- Проверка существования юзера ---

    user = await db.scalars(select(UserModel).where(UserModel.email == email,
                                                    UserModel.is_active == True))
    user = user.first()
    if not user:
        raise credentials_exception

    # --- Генерируем новый access-token ---
    access_token = create_access_token(data={"sub": user.email,
                                             "role": user.role,
                                             "id": user.id})
    return {"access_token": access_token,
            "token_type": "bearer"}


@router.get('/{id}', response_model=UserSchema, status_code=200)
async def get_user_by_id(id: int,
                        current_user: UserModel = Depends(get_current_admin),
                         db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает пользователя по его ID.
    """
    # --- Проверяем существование пользователя ---
    user = await db.scalars(select(UserModel).where(UserModel.id == id,
                                                    UserModel.is_active == True))
    user = user.first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

