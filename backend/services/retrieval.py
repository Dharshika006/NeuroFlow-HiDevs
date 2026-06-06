from backend.monitoring.tracing import tracer


class RetrievalService:

    async def retrieve(
        self,
        query: str,
        pipeline_id: str = "default",
        run_id: str = "unknown"
    ):

        with tracer.start_as_current_span(
            "retrieval.pipeline"
        ) as span:

            span.set_attribute(
                "pipeline_id",
                pipeline_id
            )

            span.set_attribute(
                "run_id",
                run_id
            )

            with tracer.start_as_current_span(
                "retrieval.dense"
            ):
                dense_results = []

            with tracer.start_as_current_span(
                "retrieval.sparse"
            ):
                sparse_results = []

            with tracer.start_as_current_span(
                "retrieval.metadata"
            ):
                metadata_results = []

            with tracer.start_as_current_span(
                "retrieval.fusion"
            ):
                fused_results = (
                    dense_results
                    + sparse_results
                    + metadata_results
                )

            with tracer.start_as_current_span(
                "retrieval.rerank"
            ):
                reranked_results = fused_results

            with tracer.start_as_current_span(
                "retrieval.assemble"
            ):
                context = {
                    "query": query,
                    "results": reranked_results
                }

            return context