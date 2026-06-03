import json
import asyncio
import time

from fastapi import APIRouter

from sse_starlette.sse import EventSourceResponse

from pipelines.retrieval.pipeline import RetrievalPipeline
from pipelines.generation.generator import Generator

router = APIRouter()

retrieval_pipeline = RetrievalPipeline()

generator = Generator()


@router.post("/query")
async def query(payload: dict):

    query_text = payload["query"]

    return {
        "status": "ready",
        "query": query_text
    }


@router.get("/query/{query_text}/stream")
async def stream(query_text: str):

    async def event_generator():

        last_keepalive = time.time()

        # =========================
        # Retrieval start
        # =========================

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

        # =========================
        # Streaming generation
        # =========================

        async for event in generator.generate(

            query=query_text,

            retrieval_result=retrieval

        ):

            now = time.time()

            # keepalive every 15s
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