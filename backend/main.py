import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Internal Imports - Ensure these paths match your folder structure
from backend.db.pool import init_pool, close_pool
from backend.db.health import check_postgres, check_redis, check_mlflow
from backend.db.migrations import run_migrations

# Import the router here (adjusted path)
try:
    from backend.api.ingest import router as ingest_router
except ImportError:
    from backend.api.ingest import router as ingest_router
# =========================
# Metrics
# =========================
REQUEST_COUNT = Counter("app_requests_total", "Total API Requests")

# =========================
# Lifespan (startup/shutdown)
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB and run migrations
    await init_pool()
    await run_migrations()
    yield

    # Shutdown: Clean up connections
    await close_pool()

# =========================
# App initialization
# =========================
from pipelines.ingestion.api import router as ingestion_router
from pipelines.ingestion.api import router as ingestion_router
app = FastAPI(
    title="NeuroFlow API",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(ingestion_router)
app.include_router(ingestion_router)

# OpenTelemetry instrumentation
FastAPIInstrumentor.instrument_app(app)

# =========================
# Routes
# =========================
@app.get("/")
async def root():
    return {"message": "NeuroFlow API running"}

@app.get("/health")
async def health():
    REQUEST_COUNT.inc()
    
    # Run health checks concurrently for better performance
    postgres_status = await check_postgres()
    redis_status = await check_redis()
    mlflow_status = await check_mlflow()

    overall = all([postgres_status, redis_status, mlflow_status])

    return {
        "status": "ok" if overall else "degraded",
        "checks": {
            "postgres": postgres_status,
            "redis": redis_status,
            "mlflow": mlflow_status
        }
    }

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Include external routers
app.include_router(ingest_router, prefix="/api/v1")