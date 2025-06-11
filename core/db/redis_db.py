import redis.asyncio as redis
from core.config.settings import env


# pool = redis.ConnectionPool.from_url(env.REDIS_URL, decode_responses=True)
# redis_client = redis.Redis(connection_pool=pool)

class RedisClient:

	session = redis.Redis.from_url(env.REDIS_URL, decode_responses=True)
	permission = redis.Redis.from_url(env.REDIS_URL, decode_responses=True)