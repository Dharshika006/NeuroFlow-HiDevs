# ADR 002: Chunking Strategy

## Context

The ingestion subsystem must split documents into chunks before embedding.
Chunking strategy directly affects retrieval quality, context coherence, and token efficiency.

Options considered:

1. Fixed-size chunking (e.g., 500 tokens)
2. Sentence-boundary chunking
3. Semantic chunking (embedding-based splitting)

## Decision

We adopt a **hybrid chunking strategy**:

* Default: **Fixed-size chunks (400–600 tokens) with overlap**
* Enhancement: **Sentence-boundary alignment**
* Advanced mode: **Semantic chunking for complex documents**

## Consequences

### Positive

* Balanced performance and simplicity
* Overlap preserves context continuity
* Sentence alignment improves readability
* Semantic chunking improves retrieval for dense/complex text

### Negative

* Slight increase in processing complexity
* Overlap increases storage usage
* Semantic chunking adds computational overhead

### Switching Conditions

We switch to semantic chunking when:

* Documents are highly unstructured (e.g., research papers)
* Context coherence is critical
* Retrieval precision drops below threshold

### Trade-offs

Fixed chunking is fast and scalable, while semantic chunking is accurate but expensive.
The hybrid approach ensures adaptability across document types.

---
