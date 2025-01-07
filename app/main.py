from fastapi import FastAPI
from app.auth.routes import auth_router


app = FastAPI()

# Подключение маршрутов
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
