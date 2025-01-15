from fastapi import FastAPI
from app.auth.routes import auth_router
from app.auth.middleware import AuthMiddleware

app = FastAPI()

# Подключение маршрутов
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Регистрируем middleware
app.add_middleware(AuthMiddleware)
