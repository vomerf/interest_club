from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.auth.utils import decode_access_token
from starlette.status import HTTP_401_UNAUTHORIZED


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Список публичных маршрутов
        public_routes = ["/login", "/register", "/docs", "/openapi.json"]

        # Проверка, является ли текущий маршрут публичным
        if request.url.path in public_routes:
            return await call_next(request)

        # Проверка наличия токена
        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse(
                {"detail": "Пользователь не авторизован"},
                status_code=HTTP_401_UNAUTHORIZED
            )

        # Проверка токена
        data = decode_access_token(token.split("Bearer ")[-1])
        if isinstance(data, JSONResponse):
            return data
        # Передача запроса следующему обработчику
        return await call_next(request)
