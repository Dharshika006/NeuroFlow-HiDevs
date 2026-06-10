import os
import redis.asyncio as redis


class RateLimiter:

    def __init__(self):

        self.redis = redis.Redis(
            host="localhost",
            port=6379,
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True
        )

    async def consume(

        self,

        bucket,

        capacity,

        refill_per_second

    ):

        key = f"rpb:{bucket}:tokens"

        tokens = await self.redis.get(key)

        if tokens is None:

            tokens = capacity

        tokens = float(tokens)

        if tokens < 1:

            return False

        await self.redis.set(
            key,
            tokens - 1
        )

        return True