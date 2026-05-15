import os
import uuid

from dotenv import load_dotenv

load_dotenv()

from fastapi import APIRouter, UploadFile, File
from arq import create_pool
from arq.connections import RedisSettings

from pipelines.ingestion.utils import compute_sha256

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):

    content = await file.read()

    content_hash = compute_sha256(content)

    document_id = str(uuid.uuid4())

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{document_id}_{file.filename}"
    )

    with open(file_path, "wb") as f:
        f.write(content)

    redis = await create_pool(
        RedisSettings(
            host="localhost",
            port=6379,
            password=os.getenv("REDIS_PASSWORD")
        )
    )

    existing = await redis.get(f"hash:{content_hash}")

    if existing:
        return {
            "document_id": existing,
            "status": "duplicate",
            "duplicate": True
        }

    await redis.set(
        f"hash:{content_hash}",
        document_id
    )

    await redis.enqueue_job(
        "process_document",
        document_id,
        file_path
    )

    return {
        "document_id": document_id,
        "status": "queued",
        "duplicate": False
    }


@router.get("/documents/{document_id}")
async def get_document(document_id: str):

    redis = await create_pool(
        RedisSettings(
            host="localhost",
            port=6379,
            password=os.getenv("REDIS_PASSWORD")
        )
    )

    status = await redis.get(
        f"document:{document_id}:status"
    )

    chunks = await redis.get(
        f"document:{document_id}:chunks"
    )

    return {
        "document_id": document_id,
        "status": status,
        "chunk_count": chunks
    }