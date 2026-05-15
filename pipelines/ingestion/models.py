from dataclasses import dataclass
import os
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ExtractedPage:
    page_number: int
    content: str
    content_type: str
    metadata: dict

import redis.asyncio as RedisSettings

def get_redis():
    return RedisSettings(
        host="localhost",
        port=6379,
        password=os.getenv("REDIS_PASSWORD"),
        
    )