from collections import defaultdict
from typing import DefaultDict


def reciprocal_rank_fusion(
    result_lists,
    k: int = 60
):

    scores: DefaultDict[str, float] = defaultdict(float)

    chunk_map = {}

    for results in result_lists:

        for rank, result in enumerate(results):

            scores[result.chunk_id] += 1 / (k + rank + 1)

            chunk_map[result.chunk_id] = result

    reranked = sorted(
        chunk_map.values(),
        key=lambda r: scores[r.chunk_id],
        reverse=True
    )

    return reranked