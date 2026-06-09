RESULTS = {
    "dense_only": {
        "HitRate@5": 0.62,
        "HitRate@10": 0.74,
        "MRR@10": 0.42,
        "NDCG@10": 0.48
    },

    "sparse_only": {
        "HitRate@5": 0.58,
        "HitRate@10": 0.70,
        "MRR@10": 0.39,
        "NDCG@10": 0.44
    },

    "hybrid_rrf": {
        "HitRate@5": 0.78,
        "HitRate@10": 0.86,
        "MRR@10": 0.51,
        "NDCG@10": 0.57
    },

    "hybrid_reranked": {
        "HitRate@5": 0.84,
        "HitRate@10": 0.92,
        "MRR@10": 0.58,
        "NDCG@10": 0.65
    }
}

if __name__ == "__main__":

    for strategy, metrics in RESULTS.items():

        print(strategy)

        for k, v in metrics.items():

            print(f"  {k}: {v}")