from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

# Получаем URL для подключения к базе данных

# Создаем движок SQLAlchemy
engine = create_engine(settings.db.DATABASE_URL)


# Создаем базовый класс для моделей
class Base(DeclarativeBase):
    pass


# Создаем сессию для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Функция для получения текущей сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
