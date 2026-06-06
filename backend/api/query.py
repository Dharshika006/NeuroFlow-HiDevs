import json
import asyncio
import time

from fastapi import APIRouter

from sse_starlette.sse import EventSourceResponse

from pipelines.retrieval.pipeline import RetrievalPipeline
from pipelines.generation.generator import Generator

from backend.monitoring.metrics import (
    queries_total
)

router = APIRouter()

retrieval_pipeline = RetrievalPipeline()

generator = Generator()


@router.post("/query")
async def query(payload: dict):

    query_text = payload["query"]

    pipeline_id = payload.get(
        "pipeline_id",
        "default"
    )

    try:

        queries_total.labels(
            pipeline_id,
            "success"
        ).inc()

        return {
            "status": "ready",
            "query": query_text
        }

    except Exception:

        queries_total.labels(
            pipeline_id,
            "error"
        ).inc()

        raise


@router.get("/query/{query_text}/stream")
async def stream(query_text: str):

    async def event_generator():

        last_keepalive = time.time()

        yield {
            "data": json.dumps({
                "type": "retrieval_start"
            })
        }

        retrieval = await retrieval_pipeline.build_context(
            query_text
        )

        yield {
            "data": json.dumps({
                "type": "retrieval_complete",
                "chunk_count": len(
                    retrieval["chunks_used"]
                ),
                "sources": retrieval["sources"]
            })
        }

        async for event in generator.generate(

            query=query_text,

            retrieval_result=retrieval

        ):

            now = time.time()

            if now - last_keepalive > 15:

                yield {
                    "data": json.dumps({
                        "type": "keepalive"
                    })
                }

                last_keepalive = now

            yield {
                "data": json.dumps(event)
            }

            await asyncio.sleep(0)

    return EventSourceResponse(
        event_generator()
    )