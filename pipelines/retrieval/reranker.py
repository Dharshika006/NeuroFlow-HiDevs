from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    async def rerank(self, query, candidates):

        pairs = [
            (query, c.content)
            for c in candidates
        ]

        scores = self.model.predict(pairs)

        for c, score in zip(candidates, scores):

            c.score = float(score)

        return sorted(
            candidates,
            key=lambda x: x.score,
            reverse=True
        )