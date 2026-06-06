from backend.monitoring.tracing import tracer

with tracer.start_as_current_span(
    "generation.pipeline"
):

    with tracer.start_as_current_span(
        "generation.prompt_build"
    ):
        prompt = ...

    with tracer.start_as_current_span(
        "generation.llm_call"
    ):
        response = ...

    with tracer.start_as_current_span(
        "generation.citation_parse"
    ):
        citations = ...

    with tracer.start_as_current_span(
        "generation.log_run"
    ):
        ...