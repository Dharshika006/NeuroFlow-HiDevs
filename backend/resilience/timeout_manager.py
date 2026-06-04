import asyncio
import os

import redis.asyncio as redis

from backend.resilience.adaptive_timeout import (
    AdaptiveTimeoutManager
)


timeouts = {

    "embedding": 10,

    "chat_completion": 60,

    "reranking": 15,

    "evaluation": 120,

    "file_extraction": 30,

    "url_fetch": 15
}


class TimeoutManager:

    def __init__(self):

        self.redis = redis.Redis(

            host="localhost",

            port=6379,

            password=os.getenv(
                "REDIS_PASSWORD"
            ),

            decode_responses=True
        )

        self.adaptive = (
            AdaptiveTimeoutManager()
        )

    async def run(

        self,

        coro,

        task_type

    ):

        try:

            adaptive_timeout = (

                await self.adaptive
                .get_timeout(

                    task_type,

                    timeouts[
                        task_type
                    ]
                )
            )

            start = (
                asyncio
                .get_event_loop()
                .time()
            )

            result = await asyncio.wait_for(

                coro,

                timeout=
                adaptive_timeout
            )

            latency_ms = (

                asyncio
                .get_event_loop()
                .time()

                - start

            ) * 1000

            await self.adaptive.record_latency(

                task_type,

                latency_ms
            )

            return result

        except asyncio.TimeoutError:

            await self.redis.incr(

                f"timeouts:{task_type}"
            )

            raise