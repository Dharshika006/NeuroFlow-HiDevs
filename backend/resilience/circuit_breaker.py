import time
import os
import redis.asyncio as redis

from contextlib import asynccontextmanager


class CircuitOpenError(Exception):
    pass


class CircuitBreaker:

    def __init__(
        self,
        name,
        failure_threshold=5,
        recovery_timeout=60,
        half_open_max_calls=3
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls

        self.redis = redis.Redis(
            host="localhost",
            port=6379,
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True
        )

    async def state(self):
        return await self.redis.get(
            f"circuit:{self.name}:state"
        ) or "closed"

    async def failure_count(self):
        return int(
            await self.redis.get(
                f"circuit:{self.name}:failure_count"
            ) or 0
        )

    async def record_success(self):

        await self.redis.set(
            f"circuit:{self.name}:state",
            "closed"
        )

        await self.redis.set(
            f"circuit:{self.name}:failure_count",
            0
        )

    async def record_failure(self):

        count = await self.failure_count()

        count += 1

        await self.redis.set(
            f"circuit:{self.name}:failure_count",
            count
        )

        if count >= self.failure_threshold:

            await self.redis.set(
                f"circuit:{self.name}:state",
                "open"
            )

            await self.redis.set(
                f"circuit:{self.name}:opened_at",
                int(time.time())
            )

    @asynccontextmanager
    async def protect(self):

        state = await self.state()

        if state == "open":

            opened = int(
                await self.redis.get(
                    f"circuit:{self.name}:opened_at"
                ) or 0
            )

            if time.time() - opened > self.recovery_timeout:

                await self.redis.set(
                    f"circuit:{self.name}:state",
                    "half_open"
                )

            else:
                raise CircuitOpenError(self.name)

        try:

            yield

            await self.record_success()

        except Exception:

            await self.record_failure()

            raise