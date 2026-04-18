# ADR 001: Vector Store Selection

## Context

NeuroFlow requires a vector database to store embeddings and support efficient similarity search for the retrieval subsystem.

Key requirements:

* Tight integration with metadata filtering
* Low operational complexity
* Cost efficiency (early-stage system)
* Support for hybrid search (vector + structured queries)

Options considered:

* Pinecone (managed, proprietary)
* Weaviate (feature-rich, standalone)
* Qdrant (high-performance vector DB)
* pgvector (PostgreSQL extension)

## Decision

We choose **pgvector** as the primary vector store.

## Consequences

### Positive

* Seamless integration with PostgreSQL (single database for vectors + metadata)
* Lower infrastructure cost (self-hosted)
* Simplified architecture (no separate vector DB service)
* Strong transactional guarantees and consistency
* Easier joins between embeddings and metadata

### Negative

* Lower horizontal scalability compared to dedicated vector databases
* Requires manual indexing and performance tuning
* Limited advanced vector search features compared to specialized systems

### Trade-offs

pgvector is ideal for early-stage systems prioritizing simplicity and cost.
If scale exceeds limits (e.g., >10M vectors), migration to Qdrant or Weaviate will be considered.

---
