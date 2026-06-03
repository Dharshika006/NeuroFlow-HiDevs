import json
import asyncio

from pipelines.retrieval.pipeline import RetrievalPipeline


test_set = [
    {
        "query": "What is HNSW indexing?",
        "relevant_chunk_ids": ["1"]
    },
    {
        "query": "Explain vector embeddings",
        "relevant_chunk_ids": ["2"]
    }
]


async def main():

    pipeline = RetrievalPipeline()

    hits = 0

    reciprocal_ranks = []

    for test in test_set:

        results = await pipeline.retrieve(
            test["query"],
            k=10
        )

        hit = any(
            r.chunk_id in test["relevant_chunk_ids"]
            for r in results
        )

        if hit:
            hits += 1

        rank = next(
            (
                i + 1
                for i, r in enumerate(results)
                if r.chunk_id in test["relevant_chunk_ids"]
            ),
            None
        )

        if rank:
            reciprocal_ranks.append(1 / rank)
        else:
            reciprocal_ranks.append(0)

    hit_rate = hits / len(test_set)

    mrr = sum(reciprocal_ranks) / len(test_set)

    results_json = {
        "hit_rate": hit_rate,
        "mrr": mrr
    }

    with open(
        "evaluation/retrieval_results.json",
        "w"
    ) as f:

        json.dump(results_json, f, indent=2)

    print(results_json)


asyncio.run(main())