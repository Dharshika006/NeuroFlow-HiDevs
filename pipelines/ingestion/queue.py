import os
import os
from dotenv import load_dotenv

load_dotenv()
from arq.connections import RedisSettings

import redis.asyncio as redis

def get_redis():
    return RedisSettings(
        host="localhost",
        port=6379,
        password=os.getenv("REDIS_PASSWORD"),
        
    )