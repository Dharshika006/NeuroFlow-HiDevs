import hashlib
import os
import uuid
import magic

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from arq import create_pool
from arq.connections import RedisSettings

from backend.security.auth import (
    require_scope
)

from backend.security.sanitizer import (
    sanitize_text
)

from backend.security.secret_detector import (
    redact_secrets
)

from backend.security.prompt_injection import (
    detect_prompt_injection
)

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/ingest")
async def ingest(

    file: UploadFile = File(...),

    user=Depends(
        require_scope(
            "ingest"
        )
    )
):

    content = await file.read()

    # MIME + magic byte validation

    mime = magic.from_buffer(
        content,
        mime=True
    )

    allowed = [

        "application/pdf",

        "text/plain",

        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]

    if mime not in allowed:

        return {

            "error":
            "invalid_file_type"
        }

    # Extract text

    try:

        extracted_text = content.decode(
            "utf-8",
            errors="ignore"
        )

    except Exception:

        extracted_text = ""

    # HTML sanitization

    clean_text = sanitize_text(
        extracted_text
    )

    # Prompt injection scan

    injection_metadata = detect_prompt_injection(
        clean_text
    )

    # Secret redaction

    clean_text, secret_events = redact_secrets(
        clean_text
    )

    content_hash = hashlib.sha256(
        content
    ).hexdigest()

    document_id = str(
        uuid.uuid4()
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(content)

    redis = await create_pool(

        RedisSettings(

            host="localhost",

            port=6379
        )
    )

    await redis.enqueue_job(

        "process_document",

        {
            "document_id":
            document_id,

            "file_path":
            file_path,

            "source_type":
            file.filename.split(".")[-1]
        }
    )

    return {

        "document_id":
        document_id,

        "status":
        "queued",

        "duplicate":
        False,

        "content_hash":
        content_hash,

        "secret_events":
        secret_events,

        "prompt_scan":
        injection_metadata
    }


@router.get(
    "/documents/{document_id}"
)
async def get_document(
    document_id: str
):

    return {

        "document_id":
        document_id,

        "status":
        "processing"
    }