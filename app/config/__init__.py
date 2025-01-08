from app.config.auth import AuthSettings
from app.config.db import DatabaseSettings


class Settings:
    auth = AuthSettings()
    db = DatabaseSettings()


settings = Settings()
