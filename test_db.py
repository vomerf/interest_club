from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from app.config import settings
from urllib.parse import quote

print(settings.db.DATABASE_URL)
# Экземпляр настроек для базы данных
# engine = create_engine(settings.db.DATABASE_URL)
engine = create_engine("postgresql://postgrtes:postgres@localhost:5432/postgres")

try:
    with engine.connect() as connection:
        # query = text("INSERT INTO user (name, fullname) VALUES (:name, :fullname)")
        # connection.execute(query, {"name": "john_doe", "fullname": "John Doe"})
        # connection.commit()  # Фиксируем изменения

    # Добавление пользователя в сессию


        print("Connection to the database was successful!")
        print(settings.db.DATABASE_URL)
except OperationalError as e:
    print("Failed to connect to the database.")
    print(f"Error: {e}")
