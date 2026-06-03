import os
import asyncpg

from fastapi import APIRouter

from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


@router.patch("/runs/{run_id}/rating")
async def rate_run(

    run_id: str,

    payload: dict
):

    conn = await asyncpg.connect(
        os.getenv("POSTGRES_URL")
    )

    rating = payload["rating"]

    row = await conn.fetchrow(
        """
        SELECT overall_score

        FROM evaluations

        WHERE run_id=$1
        """,
        run_id
    )

    calibration_needed = False

    if row:

        automated = row["overall_score"]

        if abs(
            automated - (rating / 5)
        ) > 0.3:

            calibration_needed = True

    await conn.execute(
        """
        UPDATE evaluations

        SET

            user_rating=$1,

            metadata=$2

        WHERE run_id=$3
        """,

        rating,

        {
            "calibration_needed":
            calibration_needed
        },

        run_id
    )

    await conn.close()

    return {
        "status": "updated"
    }