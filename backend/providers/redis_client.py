import redis.asyncio as redis
import os
from redis import asyncio as aioredis
from dotenv import load_dotenv
load_dotenv()


class RedisClient:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = redis.from_url(
                "redis://127.0.0.1:6379",
                decode_responses=True
            )
        return cls._client
    
import redis.asyncio as redis

def get_redis():
    return redis.Redis(
        host="localhost",
        port=6379,
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )