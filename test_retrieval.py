import asyncio

from pipelines.retrieval.pipeline import RetrievalPipeline


async def main():

    pipeline = RetrievalPipeline()

    results = await pipeline.retrieve(
        "What is HNSW indexing?"
    )

    for r in results:

        print("\n")
        print(r.chunk_id)
        print(r.score)
        print(r.content[:300])


asyncio.run(main())