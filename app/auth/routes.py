# Создадим черный список для невалидных токенов

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.utils import hash_password, verify_password, create_access_token
from app.auth.schemas import RegisterForm, UserResponse, Token
from app.auth.utils import decode_access_token
from app.auth.constants import oauth2_scheme
from app.database import get_session
from sqlalchemy.orm import Session
from app.auth.models import User


auth_router = APIRouter()


@auth_router.post("/register", response_model=UserResponse)
async def register(user: RegisterForm, session_db: Session = Depends(get_session)):
    """Регистрация новых пользователей."""
    if session_db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Такая почта уже существует")

    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        lastname=user.lastname,
        email=user.email,
        password=hashed_password,
        phone=user.phone
    )
    session_db.add(new_user)
    session_db.commit()
    session_db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}


@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session_db: Session = Depends(get_session)):
    # Поиск пользователя по email
    if not (user := session_db.query(User).filter(User.username == form_data.username).first()):
        raise HTTPException(status_code=400, detail=f"Нет пользователя с таким username={form_data.username}")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Создание токена
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # Добавляем токен в чёрный список, чтобы он больше не мог быть использован
    # redis_client.setex(token, 3600, "invalid")  # Чёрный список на 1 час (можно настроить время хранения)
    return {"message": "Successfully logged out"}


# Пример того что без токена, данная ручка не доступна
@auth_router.get("/protected-route")
async def protected_route():
    return {"message": "Hello, user"}
