from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.auth import hash_password, verify_password, create_access_token
from app.auth.schemas import UserCreate, UserResponse, Token

# Имитация базы данных
fake_users_db = []
auth_router = APIRouter()


@auth_router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
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
