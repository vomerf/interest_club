from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from app.config import settings
from urllib.parse import quote
import psycopg2

conn_str = "host=localhost dbname=postgres user=postgres password=postgres port=5432"
conn = psycopg2.connect(conn_str)
print("Connection successful!")
conn.close()
print(settings.db.DATABASE_URL)
# Экземпляр настроек для базы данных
# engine = create_engine(settings.db.DATABASE_URL)
engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT current_database();"))
        print(result.fetchone())
except OperationalError as e:
    print("Failed to connect to the database.")
    print(f"Error: {e}")
