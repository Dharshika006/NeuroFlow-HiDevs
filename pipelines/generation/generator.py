import os
import time
import asyncio
import asyncpg

from dotenv import load_dotenv

load_dotenv()

import redis.asyncio as redis

from backend.providers.groq_provider import GroqProvider

from pipelines.generation.prompt_builder import PromptBuilder
from pipelines.generation.citations import CitationParser


class Generator:

    def __init__(self):

        self.provider = GroqProvider()

        self.prompt_builder = PromptBuilder()

        self.citation_parser = CitationParser()

        self.redis = redis.Redis(
            host="localhost",
            port=6379,
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True
        )

    async def connect(self):

        return await asyncpg.connect(
            os.getenv("POSTGRES_URL")
        )

    async def generate(

        self,

        query,

        retrieval_result,

        query_type="factual"

    ):

        start = time.time()

        # =========================
        # Hidden reasoning
        # =========================

        reasoning_prompt = ""

        if query_type in [

            "analytical",

            "comparative"
        ]:

            reasoning_prompt = """
<think>
Reason step by step internally
before answering.
</think>
"""

        prompt = await self.prompt_builder.build(

            query=query,

            context=retrieval_result["context"],

            query_type=query_type
        )

        prompt += reasoning_prompt

        run_id = str(time.time())

        conn = await self.connect()

        # =========================
        # Initial pipeline log
        # =========================

        await conn.execute(
            """
            INSERT INTO pipeline_runs (

                id,
                prompt,
                status,
                metadata

            )

            VALUES (

                $1,
                $2,
                $3,
                $4
            )
            """,
            run_id,
            prompt,
            "running",
            {
                "query_type": query_type
            }
        )

        full_response = ""

        # =========================
        # Streaming generation
        # =========================

        async for token in self.provider.stream(prompt):

            full_response += token

            yield {
                "type": "token",
                "delta": token
            }

        # =========================
        # Parse citations
        # =========================

        citations = await self.citation_parser.parse(

            full_response,

            retrieval_result["chunks"]
        )

        latency = int(
            (time.time() - start) * 1000
        )

        # =========================
        # Final pipeline log
        # =========================

        await conn.execute(
            """
            UPDATE pipeline_runs

            SET

                generation = $1,

                model_used = $2,

                latency_ms = $3,

                status = $4

            WHERE id = $5
            """,
            full_response,
            "groq",
            latency,
            "complete",
            run_id
        )

        await conn.close()

        # =========================
        # Async evaluation enqueue
        # =========================

        asyncio.create_task(

            self.redis.lpush(

                "evaluation_queue",

                run_id
            )
        )

        # =========================
        # Final event
        # =========================

        yield {

            "type": "done",

            "run_id": run_id,

            "citations": [

                c.__dict__

                for c in citations
            ]
        }