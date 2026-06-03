import os
import asyncpg
import redis.asyncio as redis

from dotenv import load_dotenv

from pipelines.finetuning.job_manager import (
    poll_job_status
)

load_dotenv()


# =====================================================
# CHECK FINETUNE JOBS
# =====================================================

async def check_finetune_jobs(ctx):

    conn = await asyncpg.connect(
        os.getenv("POSTGRES_URL")
    )

    redis_client = redis.Redis(

        host="localhost",

        port=6379,

        password=os.getenv("REDIS_PASSWORD"),

        decode_responses=True
    )

    rows = await conn.fetch(
        """
        SELECT *

        FROM finetune_jobs

        WHERE status != 'succeeded'
        """
    )

    for row in rows:

        result = await poll_job_status(
            row["provider_job_id"]
        )

        # =========================
        # JOB SUCCEEDED
        # =========================

        if result["status"] == "succeeded":

            await conn.execute(
                """
                UPDATE finetune_jobs

                SET

                    status='succeeded'

                WHERE id=$1
                """,

                row["id"]
            )

            # =========================
            # Register model in router
            # =========================

            await redis_client.hset(

                "router:models",

                str(row["id"]),

                "fine-tuned-model"
            )

    await conn.close()

    await redis_client.close()


# =====================================================
# ARQ WORKER SETTINGS
# =====================================================

class WorkerSettings:

    functions = [
        check_finetune_jobs
    ]