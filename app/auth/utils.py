from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from fastapi import Depends
from app.auth.constants import oauth2_scheme
from app.config import settings
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

# Настройка контекста для хеширования
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.auth.SECRET_KEY,
        algorithm=settings.auth.ALGORITHM
    )


def decode_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            settings.auth.SECRET_KEY,
            algorithms=[settings.auth.ALGORITHM]
        )
        return payload  # Пока что никак не используется, в будещем возможно будем как-то использовать роли.
    except ExpiredSignatureError:
        return JSONResponse({"detail": "Истек срок действия токена"}, status_code=HTTP_401_UNAUTHORIZED)
    except JWTError:
        return JSONResponse({"detail": "Невалидный токен"}, status_code=HTTP_401_UNAUTHORIZED)
