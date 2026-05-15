import os
import json
import logging

from dotenv import load_dotenv

load_dotenv()

import redis.asyncio as redis

from arq.connections import RedisSettings

from opentelemetry import trace

from pipelines.ingestion.extractors.pdf_extractor import extract_pdf
from pipelines.ingestion.extractors.docx_extractor import extract_docx
from pipelines.ingestion.extractors.csv_extractor import extract_csv
from pipelines.ingestion.extractors.image_extractor import extract_image
from pipelines.ingestion.extractors.url_extractor import extract_url
from pipelines.ingestion.extractors.pptx_extractor import extract_pptx

from pipelines.ingestion.chunker import chunk_pages

logging.basicConfig(level=logging.INFO)

tracer = trace.get_tracer(__name__)


async def process_document(ctx, document_id: str, file_path: str):

    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )

    ext = os.path.splitext(file_path)[1].lower()

    with tracer.start_as_current_span("ingestion.process") as span:

        span.set_attribute("document_id", document_id)
        span.set_attribute("source_type", ext)

        await redis_client.set(
            f"document:{document_id}:status",
            "processing"
        )

        # =========================
        # Extraction
        # =========================

        if ext == ".pdf":

            pages = await extract_pdf(file_path)

        elif ext == ".docx":

            pages = await extract_docx(file_path)

        elif ext == ".csv":

            pages = await extract_csv(file_path)

        elif ext == ".pptx":

            pages = await extract_pptx(file_path)

        elif ext in [".png", ".jpg", ".jpeg", ".webp"]:

            pages = await extract_image(file_path)

        else:

            pages = []

        # =========================
        # Chunking
        # =========================

        chunks = chunk_pages(pages)

        page_count = len(pages)

        chunk_count = len(chunks)

        span.set_attribute("page_count", page_count)
        span.set_attribute("chunk_count", chunk_count)
        span.set_attribute("embedding_calls", chunk_count)

        # =========================
        # Save metrics/status
        # =========================

        await redis_client.set(
            f"document:{document_id}:chunks",
            chunk_count
        )

        await redis_client.set(
            f"document:{document_id}:status",
            "complete"
        )

        # =========================
        # Structured logs
        # =========================

        logging.info(json.dumps({
            "event": "ingestion_complete",
            "document_id": document_id,
            "page_count": page_count,
            "chunks": chunk_count
        }))

        return {
            "status": "complete",
            "document_id": document_id
        }


class WorkerSettings:

    functions = [process_document]

    redis_settings = RedisSettings(
        host="localhost",
        port=6379,
        password=os.getenv("REDIS_PASSWORD")
    )