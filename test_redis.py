import redis
from redis.exceptions import ConnectionError

# Конфигурация Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Подключение к Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

try:
    # Пытаемся выполнить команду ping
    response = r.ping()
    if response:
        print("Connected to Redis successfully!")
except ConnectionError:
    print("Failed to connect to Redis.")
