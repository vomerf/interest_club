# Создадим черный список для невалидных токенов

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.utils import hash_password, verify_password, create_access_token
from app.auth.schemas import RegisterForm, UserResponse, Token
from app.auth.utils import decode_access_token
from app.auth.constants import oauth2_scheme


# Имитация базы данных


fake_users_db = []
auth_router = APIRouter()


@auth_router.post("/register", response_model=UserResponse)
def register(user: RegisterForm):
    # Проверка на уникальность email
    if any(u["email"] == user.email for u in fake_users_db):
        raise HTTPException(status_code=400, detail="Такая почта уже существует")

    # Хеширование пароля
    hashed_password = hash_password(user.password)
    user_dict = {"id": len(fake_users_db) + 1, "email": user.email, "password": hashed_password}
    fake_users_db.append(user_dict)
    return {"id": user_dict["id"], "email": user_dict["email"]}


@auth_router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Поиск пользователя по email
    user = next((u for u in fake_users_db if u["email"] == form_data.username), None)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Создание токена
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    # Добавляем токен в чёрный список, чтобы он больше не мог быть использован
    # redis_client.setex(token, 3600, "invalid")  # Чёрный список на 1 час (можно настроить время хранения)
    return {"message": "Successfully logged out"}


# Пример того что без токена, данная ручка не доступна
@auth_router.get("/protected-route")
def protected_route(user_id: str = Depends(decode_access_token)):
    return {"message": f"Hello, user {user_id}!"}
