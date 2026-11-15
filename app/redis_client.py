import redis
import os

redis_client = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379"),
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=None, #não corta o BRPOP
)