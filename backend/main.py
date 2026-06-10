from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import Response
from backend.api.evaluations import (
    router as evaluations_router
)
from backend.api.auth import (
    router as auth_router
)

from prometheus_client import (
    Counter,
    generate_latest,
    CONTENT_TYPE_LATEST
)

from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor
)

from backend.api.query import (
    router as query_router
)

from backend.api.ratings import (
    router as ratings_router
)

from backend.api.finetune import (
    router as finetune_router
)

from backend.api.pipelines import (
    router as pipelines_router
)

from backend.api.compare import (
    router as compare_router
)

from backend.db.pool import (
    init_pool,
    close_pool
)

from backend.db.health import (
    check_postgres,
    check_redis,
    check_mlflow
)

from backend.db.migrations import (
    run_migrations
)

from backend.resilience.circuit_breaker import (
    CircuitBreaker
)

try:
    from backend.api.ingest import (
        router as ingest_router
    )
except ImportError:
    from backend.api.ingest import (
        router as ingest_router
    )

from pipelines.ingestion.api import (
    router as ingestion_router
)
from backend.security.middleware import (
    SecurityHeadersMiddleware
)


# =========================
# Metrics
# =========================

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total API Requests"
)

# =========================
# Lifespan
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_pool()

    await run_migrations()

    yield

    await close_pool()

# =========================
# FastAPI App
# =========================

app = FastAPI(

    title="NeuroFlow API",

    version="1.0.0",

    lifespan=lifespan
)

# =========================
# Routers
# =========================

app.include_router(ingestion_router)

app.include_router(query_router)

app.include_router(ratings_router)

app.include_router(pipelines_router)

app.include_router(finetune_router)

app.include_router(compare_router)

app.include_router(auth_router)

app.include_router(
    ingest_router,
    prefix="/api/v1"
)
app.add_middleware(
    SecurityHeadersMiddleware
)

app.include_router(
    evaluations_router
)
# =========================
# OpenTelemetry
# =========================

FastAPIInstrumentor.instrument_app(app)

# =========================
# Routes
# =========================

@app.get("/")
async def root():

    return {
        "message":
        "NeuroFlow API running"
    }

@app.get("/health")
async def health():

    REQUEST_COUNT.inc()

    postgres_status = await check_postgres()

    redis_status = await check_redis()

    mlflow_status = await check_mlflow()

    openai_cb = CircuitBreaker(
        "openai"
    )

    cb_state = await openai_cb.state()

    cb_failures = await openai_cb.failure_count()

    overall = all([
        postgres_status,
        redis_status,
        mlflow_status
    ])

    return {

        "status":

            "degraded"

            if cb_state == "open"

            else (

                "ok"

                if overall

                else "critical"
            ),

        "checks": {

            "postgres":
            postgres_status,

            "redis":
            redis_status,

            "mlflow":
            mlflow_status,

            "circuit_breakers": {

                "openai": {

                    "state":
                    cb_state,

                    "failure_count":
                    cb_failures
                }
            }
        }
    }

@app.get("/metrics")
async def metrics():

    return Response(

        generate_latest(),

        media_type=
        CONTENT_TYPE_LATEST
    )

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)