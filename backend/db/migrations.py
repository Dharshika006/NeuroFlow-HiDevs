import asyncpg
from backend.config import settings

# Required tables for base schema
REQUIRED_TABLES = {
    "documents",
    "chunks",
    "pipelines",
    "pipeline_runs",
    "evaluations",
    "training_pairs",
    "finetune_jobs",
}

async def check_tables(conn):
    rows = await conn.fetch(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
        """
    )
    existing = {r["table_name"] for r in rows}
    return REQUIRED_TABLES.issubset(existing)

async def apply_migration(conn):
    # =========================
    # Ensure extensions
    # =========================
    await conn.execute("""
        CREATE EXTENSION IF NOT EXISTS vector;
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    """)

    # =========================
    # Add missing columns safely
    # =========================
    await conn.execute("""
        ALTER TABLE chunks
        ADD COLUMN IF NOT EXISTS embedding vector(1536);
    """)

    await conn.execute("""
        ALTER TABLE chunks
        ADD COLUMN IF NOT EXISTS chunk_index INT;
    """)

    await conn.execute("""
        ALTER TABLE chunks
        ADD COLUMN IF NOT EXISTS token_count INT;
    """)

    await conn.execute("""
        ALTER TABLE chunks
        ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}';
    """)

    await conn.execute("""
        ALTER TABLE chunks
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW();
    """)

    # =========================
    # Fix existing data safely
    # =========================
    await conn.execute("""
        UPDATE chunks
        SET chunk_index = 0
        WHERE chunk_index IS NULL;
    """)

    await conn.execute("""
        UPDATE chunks
        SET token_count = LENGTH(content)
        WHERE token_count IS NULL;
    """)

    # =========================
    # Add NOT NULL constraints
    # =========================
    await conn.execute("""
        ALTER TABLE chunks
        ALTER COLUMN chunk_index SET NOT NULL;
    """)

    await conn.execute("""
        ALTER TABLE chunks
        ALTER COLUMN token_count SET NOT NULL;
    """)

    # =========================
    # Create indexes safely
    # =========================
    await conn.execute("""
        CREATE INDEX IF NOT EXISTS chunks_embedding_idx
        ON chunks USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);
    """)

    await conn.execute("""
        CREATE INDEX IF NOT EXISTS chunks_document_idx
        ON chunks (document_id);
    """)

    await conn.execute("""
        CREATE INDEX IF NOT EXISTS chunks_content_idx
        ON chunks USING gin (to_tsvector('english', content));
    """)

async def run_migrations():
    conn = await asyncpg.connect(settings.postgres_url)
    try:
        tables_ok = await check_tables(conn)

        if not tables_ok:
            print("❌ Base schema missing. Run 001_schema.sql first.")
            return

        print("✅ Tables exist. Applying migrations...")

        await apply_migration(conn)

        print("✅ Migration completed successfully")

    except Exception as e:
        print(f"❌ Migration failed: {e}")

    finally:
        await conn.close()