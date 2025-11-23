from redis.asyncio import Redis
import os

REDIS_URI = os.getenv("REDIS_URI")

redis = Redis.from_url(REDIS_URI, decode_responses=True)


async def get_redis():
    return redis
