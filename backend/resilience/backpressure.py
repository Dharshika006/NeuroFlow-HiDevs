import redis.asyncio as redis
import os

async def check_ingestion_queue():

    r = redis.Redis(
        host="localhost",
        port=6379,
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )

    depth = await r.llen(
        "queue:ingest"
    )

    if depth > 100:

        return {

            "status": 503,

            "error":
            "ingestion_queue_full",

            "queue_depth":
            depth,

            "retry_after":
            30
        }

    if depth > 50:

        return {

            "status": 202,

            "warning":
            "high_queue_depth",

            "estimated_wait_minutes":
            depth // 10
        }

    return {

        "status": 200
    }