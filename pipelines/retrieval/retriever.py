import os
import asyncio

from dotenv import load_dotenv

load_dotenv()

import asyncpg

from sentence_transformers import SentenceTransformer

from pipelines.retrieval.models import RetrievalResult
from pipelines.retrieval.fusion import reciprocal_rank_fusion


class Retriever:

    def __init__(self):

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    async def connect(self):

        return await asyncpg.connect(
            os.getenv("POSTGRES_URL")
        )

    # =========================
    # Dense retrieval
    # =========================

    async def _dense_retrieval(
        self,
        query,
        k=20
    ):

        conn = await self.connect()

        embedding = self.embedding_model.encode(
            query
        ).tolist()

        # pgvector expects string
        embedding = str(embedding)

        rows = await conn.fetch(
            """
            SELECT
                id,
                content,
                metadata,
                embedding <=> $1::vector AS distance
            FROM chunks
            ORDER BY embedding <=> $1::vector
            LIMIT $2
            """,
            embedding,
            k
        )

        await conn.close()

        return [

            RetrievalResult(
                chunk_id=str(row["id"]),
                content=row["content"],
                score=float(row["distance"]),
                metadata=row["metadata"]
            )

            for row in rows
        ]

    # =========================
    # Sparse retrieval
    # =========================

    async def _sparse_retrieval(
        self,
        query,
        k=20
    ):

        conn = await self.connect()

        rows = await conn.fetch(
            """
            SELECT
                id,
                content,
                metadata,

                ts_rank_cd(
                    to_tsvector(
                        'english',
                        content
                    ),

                    plainto_tsquery(
                        'english',
                        $1
                    )

                ) AS rank

            FROM chunks

            WHERE

                to_tsvector(
                    'english',
                    content
                )

                @@ plainto_tsquery(
                    'english',
                    $1
                )

            ORDER BY rank DESC

            LIMIT $2
            """,
            query,
            k
        )

        await conn.close()

        return [

            RetrievalResult(
                chunk_id=str(row["id"]),
                content=row["content"],
                score=float(row["rank"]),
                metadata=row["metadata"]
            )

            for row in rows
        ]

    # =========================
    # Metadata retrieval
    # =========================

    async def _metadata_retrieval(
        self,
        query,
        filters,
        k=20
    ):

        if not filters:
            return []

        conn = await self.connect()

        embedding = self.embedding_model.encode(
            query
        ).tolist()

        embedding = str(embedding)

        rows = await conn.fetch(
            """
            SELECT
                id,
                content,
                metadata

            FROM chunks

            WHERE metadata @> $1::jsonb

            ORDER BY embedding <=> $2::vector

            LIMIT $3
            """,
            str(filters),
            embedding,
            k
        )

        await conn.close()

        return [

            RetrievalResult(
                chunk_id=str(row["id"]),
                content=row["content"],
                score=1.0,
                metadata=row["metadata"]
            )

            for row in rows
        ]

    # =========================
    # Main retrieval
    # =========================

    async def retrieve(
        self,
        query,
        filters=None,
        k=20
    ):

        results = await asyncio.gather(

            self._dense_retrieval(
                query,
                k
            ),

            self._sparse_retrieval(
                query,
                k
            ),

            self._metadata_retrieval(
                query,
                filters,
                k
            )
        )

        fused = reciprocal_rank_fusion(
            results
        )

        return fused[:k]