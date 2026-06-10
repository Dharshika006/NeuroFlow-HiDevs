import os
import time

import redis.asyncio as redis

from dotenv import load_dotenv

load_dotenv()


class AdaptiveTimeoutManager:

    def __init__(self):

        self.redis = redis.Redis(
            host="localhost",
            port=6379,
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True
        )

    async def record_latency(

        self,

        task_type,

        latency_ms
    ):

        key = f"latency:{task_type}"

        await self.redis.zadd(
            key,
            {
                str(time.time()):
                latency_ms
            }
        )

        await self.redis.zremrangebyrank(
            key,
            0,
            -1001
        )

    async def get_timeout(

        self,

        task_type,

        default_timeout
    ):

        key = f"latency:{task_type}"

        values = await self.redis.zrange(
            key,
            0,
            -1,
            withscores=True
        )

        if len(values) < 20:

            return default_timeout

        latencies = [

            score

            for _, score

            in values
        ]

        latencies.sort()

        p95_index = int(
            len(latencies) * 0.95
        )

        p95 = latencies[p95_index]

        timeout_seconds = (

            p95 / 1000
        ) * 1.5

        return max(
            default_timeout,
            timeout_seconds
        )