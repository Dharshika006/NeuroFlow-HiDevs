import os
import asyncpg

from fastapi import (
    APIRouter,
    Depends
)

from dotenv import load_dotenv

from backend.security.auth import (
    require_scope
)

from pipelines.finetuning.extractor import (
    TrainingExtractor
)

from pipelines.finetuning.tracker import (
    start_training_job
)

from pipelines.finetuning.job_manager import (

    submit_finetune_job,

    poll_job_status
)

load_dotenv()

router = APIRouter()


async def connect():

    return await asyncpg.connect(
        os.getenv("POSTGRES_URL")
    )


# =====================================================
# CREATE JOB
# =====================================================

@router.post("/finetune/jobs")
async def create_job(

    user=Depends(
        require_scope(
            "admin"
        )
    )
):

    extractor = TrainingExtractor()

    result = await extractor.extract()

    job_id = result["job_id"]

    jsonl_path = result["path"]

    pairs = result["pairs"]

    mlflow_run_id = start_training_job(

        job_id,

        pairs,

        jsonl_path
    )

    provider_job_id = await submit_finetune_job(

        jsonl_path,

        "gpt-4o-mini"
    )

    conn = await connect()

    await conn.execute(
        """
        INSERT INTO finetune_jobs (

            id,
            status,
            provider_job_id,
            mlflow_run_id,
            base_model,
            training_pair_count

        )

        VALUES (

            $1,$2,$3,$4,$5,$6
        )
        """,

        job_id,

        "submitted",

        provider_job_id,

        mlflow_run_id,

        "gpt-4o-mini",

        len(pairs)
    )

    await conn.close()

    return {

        "job_id":
        job_id,

        "provider_job_id":
        provider_job_id
    }


# =====================================================
# LIST JOBS
# =====================================================

@router.get("/finetune/jobs")
async def list_jobs():

    conn = await connect()

    rows = await conn.fetch(
        """
        SELECT *

        FROM finetune_jobs

        ORDER BY created_at DESC
        """
    )

    await conn.close()

    return [

        dict(r)

        for r in rows
    ]


# =====================================================
# GET JOB
# =====================================================

@router.get("/finetune/jobs/{job_id}")
async def get_job(

    job_id: str
):

    conn = await connect()

    row = await conn.fetchrow(
        """
        SELECT *

        FROM finetune_jobs

        WHERE id=$1
        """,
        job_id
    )

    await conn.close()

    if not row:

        return {

            "error":
            "job_not_found"
        }

    return dict(row)


# =====================================================
# PREVIEW TRAINING DATA
# =====================================================

@router.get("/finetune/training-data/preview")
async def preview():

    extractor = TrainingExtractor()

    result = await extractor.extract()

    return result["pairs"][:5]


# =====================================================
# DPO PREVIEW
# =====================================================

@router.get("/finetune/dpo-preview")
async def dpo_preview():

    extractor = TrainingExtractor()

    pairs = await extractor.extract_dpo_pairs()

    return pairs[:5]


# =====================================================
# CHECK FINETUNE STATUS
# =====================================================

@router.post("/finetune")
async def finetune(

    payload: dict,

    user=Depends(
        require_scope(
            "admin"
        )
    )
):

    job_id = payload.get(
        "job_id"
    )

    if not job_id:

        return {

            "error":
            "job_id is required"
        }

    status = await poll_job_status(
        job_id
    )

    return {

        "job_id":
        job_id,

        "status":
        status
    }