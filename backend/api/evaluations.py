from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

import asyncio
import json

router = APIRouter()


@router.get("/evaluations/stream")
async def stream_evaluations():

    async def generator():

        while True:

            yield {
                "data": json.dumps(
                    {
                        "query": "Test Query",
                        "faithfulness": 0.91,
                        "answer_relevance": 0.88,
                        "context_precision": 0.86,
                        "context_recall": 0.89,
                        "overall_score": 0.89
                    }
                )
            }

            await asyncio.sleep(10)

    return EventSourceResponse(generator())

