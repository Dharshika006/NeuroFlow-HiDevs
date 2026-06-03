from pipelines.retrieval.query_processor import QueryProcessor
from pipelines.retrieval.retriever import Retriever
from pipelines.retrieval.reranker import Reranker
from pipelines.retrieval.context_assembler import ContextAssembler
from pipelines.retrieval.hyde import HyDEGenerator


class RetrievalPipeline:

    def __init__(self):

        self.query_processor = QueryProcessor()

        self.retriever = Retriever()

        self.reranker = Reranker()

        self.context_assembler = ContextAssembler()

        self.hyde = HyDEGenerator()

    async def retrieve(
        self,
        query,
        k=10
    ):

        # =========================
        # Query processing
        # =========================

        expanded_queries = (
            await self.query_processor.expand_query(
                query
            )
        )

        metadata_filters = (
            await self.query_processor.extract_metadata_filters(
                query
            )
        )

        query_type = (
            await self.query_processor.classify_query(
                query
            )
        )

        # =========================
        # HyDE query
        # =========================

        hyde_query = await self.hyde.generate(
            query
        )

        # =========================
        # Parallel retrieval
        # =========================

        all_results = []

        for q in expanded_queries:

            results = await self.retriever.retrieve(
                q,
                metadata_filters,
                k
            )

            all_results.extend(results)

        # HyDE retrieval

        hyde_results = await self.retriever.retrieve(
            hyde_query,
            metadata_filters,
            k
        )

        all_results.extend(hyde_results)

        # =========================
        # Deduplicate
        # =========================

        unique = {}

        for result in all_results:

            unique[result.chunk_id] = result

        deduped_results = list(unique.values())

        # =========================
        # Cross encoder reranking
        # =========================

        reranked = await self.reranker.rerank(
            query,
            deduped_results[:40]
        )

        return reranked[:k]

    async def build_context(
        self,
        query,
        token_budget=4000
    ):

        chunks = await self.retrieve(query)

        assembled = (
            await self.context_assembler.assemble(
                chunks,
                token_budget
            )
        )

        return {
            "query": query,
            "context": assembled["context"],
            "chunks_used": assembled["chunks_used"],
            "total_tokens": assembled["total_tokens"],
            "sources": assembled["sources"]
        }