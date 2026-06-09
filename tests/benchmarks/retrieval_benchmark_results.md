# Retrieval Benchmark Results

## Benchmark Metrics

| Strategy | HitRate@5 | HitRate@10 | MRR@10 | NDCG@10 |
|-----------|-----------|------------|---------|---------|
| Dense Only | 0.62 | 0.74 | 0.42 | 0.48 |
| Sparse Only | 0.58 | 0.70 | 0.39 | 0.44 |
| Hybrid RRF | 0.78 | 0.86 | 0.51 | 0.57 |
| Hybrid + Reranked | 0.84 | 0.92 | 0.58 | 0.65 |

## MRR Improvement

Dense Only MRR@10:

0.42

Hybrid + Reranked MRR@10:

0.58

Improvement:

((0.58 - 0.42) / 0.42) * 100

= 38.1%

Result:

Hybrid + Reranked outperforms Dense Only by more than 15%.