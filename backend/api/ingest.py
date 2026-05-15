import hashlib
import os
import uuid

from fastapi import APIRouter, UploadFile, File
from arq import create_pool
from arq.connections import RedisSettings


router = APIRouter()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    content = await file.read()

    content_hash = hashlib.sha256(content).hexdigest()

    document_id = str(uuid.uuid4())

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(content)

    redis = await create_pool(
        RedisSettings(host="localhost", port=6379)
    )

    await redis.enqueue_job(
        "process_document",
        {
            "document_id": document_id,
            "file_path": file_path,
            "source_type": file.filename.split(".")[-1]
        }
    )

    return {
        "document_id": document_id,
        "status": "queued",
        "duplicate": False,
        "content_hash": content_hash
    }


@router.get("/documents/{document_id}")
async def get_document(document_id: str):
    return {
        "document_id": document_id,
        "status": "processing"
    }