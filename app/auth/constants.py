from fastapi.security import OAuth2PasswordBearer

# Проверяет наличине токена в заголовке.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
