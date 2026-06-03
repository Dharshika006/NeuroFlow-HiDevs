from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


async def evaluate_answer_relevance(

    query,

    answer

):

    query_emb = model.encode([query])

    answer_emb = model.encode([answer])

    score = cosine_similarity(
        query_emb,
        answer_emb
    )[0][0]

    return float(max(0.0, min(score, 1.0)))