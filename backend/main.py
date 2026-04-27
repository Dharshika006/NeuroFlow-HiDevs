from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from db.pool import init_pool, close_pool
from db.health import check_postgres, check_redis, check_mlflow
from db.migrations import run_migrations

# =========================
# Metrics
# =========================
REQUEST_COUNT = Counter("app_requests_total", "Total API Requests")

# =========================
# Lifespan (startup/shutdown)
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_pool()
    await run_migrations()
    yield

    # Shutdown
    await close_pool()

# =========================
# App initialization
# =========================
app = FastAPI(lifespan=lifespan)

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