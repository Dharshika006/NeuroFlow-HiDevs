import os
import asyncpg

from fastapi import APIRouter
from fastapi import Depends

from backend.security.auth import (
    require_scope
)
from dotenv import load_dotenv

from backend.models.pipeline import (
    PipelineConfig
)

from backend.services.pipeline_optimizer import (
    PipelineOptimizer
)

load_dotenv()

router = APIRouter()

optimizer = PipelineOptimizer()


async def connect():

    return await asyncpg.connect(
        os.getenv("POSTGRES_URL")
    )


# =====================================================
# CREATE PIPELINE
# =====================================================

@router.post("/pipelines")
async def create_pipeline(

    payload: PipelineConfig
):

    conn = await connect()

    version = 1

    row = await conn.fetchrow(
        """
        INSERT INTO pipelines (

            name,
            version,
            description,
            config

        )

        VALUES (

            $1,$2,$3,$4
        )

        RETURNING id
        """,

        payload.name,

        version,

        payload.description,

        payload.model_dump()
    )

    await conn.close()

    return {
        "pipeline_id": str(row["id"])
    }


# =====================================================
# LIST PIPELINES
# =====================================================

@router.get("/pipelines")
async def list_pipelines():

    conn = await connect()

    rows = await conn.fetch(
        """
        SELECT *

        FROM pipelines

        WHERE status='active'

        ORDER BY created_at DESC
        """
    )

    await conn.close()

    return [

        dict(r)

        for r in rows
    ]


# =====================================================
# GET PIPELINE
# =====================================================

@router.get("/pipelines/{pipeline_id}")
async def get_pipeline(

    pipeline_id: str
):

    conn = await connect()

    row = await conn.fetchrow(
        """
        SELECT *

        FROM pipelines

        WHERE id=$1
        """,
        pipeline_id
    )

    await conn.close()

    return dict(row)


# =====================================================
# UPDATE PIPELINE
# =====================================================

@router.patch("/pipelines/{pipeline_id}")
async def update_pipeline(

    pipeline_id: str,

    payload: PipelineConfig
):

    conn = await connect()

    current = await conn.fetchrow(
        """
        SELECT version,name

        FROM pipelines

        WHERE id=$1
        """,
        pipeline_id
    )

    new_version = current["version"] + 1

    row = await conn.fetchrow(
        """
        INSERT INTO pipelines (

            name,
            version,
            description,
            config

        )

        VALUES (

            $1,$2,$3,$4
        )

        RETURNING id
        """,

        payload.name,

        new_version,

        payload.description,

        payload.model_dump()
    )

    await conn.close()

    return {

        "new_pipeline_id":
        str(row["id"]),

        "version":
        new_version
    }


# =====================================================
# SOFT DELETE
# =====================================================

@router.delete("/pipelines/{pipeline_id}")
async def archive_pipeline(

    pipeline_id: str
):

    conn = await connect()

    await conn.execute(
        """
        UPDATE pipelines

        SET status='archived'

        WHERE id=$1
        """,
        pipeline_id
    )

    await conn.close()

    return {
        "status": "archived"
    }


# =====================================================
# PIPELINE RUN HISTORY
# =====================================================

@router.get("/pipelines/{pipeline_id}/runs")
async def pipeline_runs(

    pipeline_id: str,

    limit: int = 10,

    offset: int = 0
):

    conn = await connect()

    rows = await conn.fetch(
        """
        SELECT *

        FROM pipeline_runs

        ORDER BY created_at DESC

        LIMIT $1

        OFFSET $2
        """,

        limit,

        offset
    )

    await conn.close()

    return [

        dict(r)

        for r in rows
    ]


# =====================================================
# ANALYTICS
# =====================================================

@router.get("/pipelines/{pipeline_id}/analytics")
async def analytics(

    pipeline_id: str
):

    conn = await connect()

    rows = await conn.fetch(
        """
        SELECT latency_ms

        FROM pipeline_runs
        """
    )

    latencies = [

        r["latency_ms"]

        for r in rows

        if r["latency_ms"]
    ]

    latencies.sort()

    def percentile(data, p):

        if not data:
            return 0

        index = int(
            len(data) * p
        )

        return data[
            min(index, len(data)-1)
        ]

    result = {

        "p50_latency":
        percentile(latencies, 0.50),

        "p95_latency":
        percentile(latencies, 0.95),

        "p99_latency":
        percentile(latencies, 0.99),

        "query_count":
        len(latencies)
    }

    # =========================
    # Cost Estimation
    # =========================

    INPUT_TOKEN_PRICE = 0.000001
    OUTPUT_TOKEN_PRICE = 0.000002

    total_cost = 0

    token_rows = await conn.fetch(
        """
        SELECT metadata

        FROM evaluations
        """
    )

    for row in token_rows:

        metadata = row["metadata"] or {}

        input_tokens = metadata.get(
            "input_tokens",
            0
        )

        output_tokens = metadata.get(
            "output_tokens",
            0
        )

        total_cost += (

            input_tokens * INPUT_TOKEN_PRICE +

            output_tokens * OUTPUT_TOKEN_PRICE
        )

    result["estimated_total_cost"] = round(
        total_cost,
        4
    )

    # =========================
    # Queries per day
    # =========================

    query_rows = await conn.fetch(
        """
        SELECT DATE(created_at) as day,
               COUNT(*) as count

        FROM pipeline_runs

        GROUP BY day

        ORDER BY day DESC

        LIMIT 30
        """
    )

    result["queries_per_day"] = [

        {
            "day": str(r["day"]),
            "count": r["count"]
        }

        for r in query_rows
    ]

    await conn.close()

    return result


# =====================================================
# PIPELINE SUGGESTIONS
# =====================================================

@router.get("/pipelines/{pipeline_id}/suggestions")
async def suggestions(

    pipeline_id: str
):

    metrics = {

        "context_precision": 0.4,

        "context_recall": 0.6,

        "faithfulness": 0.7
    }

    return {

        "suggestions":
        optimizer.suggest(metrics)
    }

@router.post("/pipelines")
async def create_pipeline(

    payload: dict,

    user=Depends(
        require_scope(
            "admin"
        )
    )
):

    # Implement pipeline creation logic here

    return {
        "message": "Pipeline created successfully"
    }