CREATE EXTENSION IF NOT EXISTS vector;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS chunks (

    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    content TEXT,

    metadata JSONB,

    embedding vector(384)
);

-- =========================
-- HNSW VECTOR INDEX
-- =========================

CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw_idx
ON chunks
USING hnsw (embedding vector_cosine_ops);

-- =========================
-- FULL TEXT SEARCH INDEX
-- =========================

CREATE INDEX IF NOT EXISTS chunks_tsv_idx
ON chunks
USING GIN(to_tsvector('english', content));

-- =========================
-- METADATA GIN INDEX
-- =========================

CREATE INDEX IF NOT EXISTS chunks_metadata_idx
ON chunks
USING GIN(metadata);