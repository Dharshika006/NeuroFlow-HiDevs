from fastapi import FastAPI
from db.pool import init_pool, close_pool
from db.health import check_postgres, check_redis

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_pool()

@app.on_event("shutdown")
async def shutdown():
    await close_pool()

@app.get("/health")
async def health():
    postgres_status = await check_postgres()
    redis_status = await check_redis()
    overall_status = "ok" if all([postgres_status, redis_status]) else "degraded"

    return {
        "status": overall_status,
        "checks": {
            "postgres": postgres_status,
            "redis": redis_status
        }
    }

@app.get("/")
async def root():
    return {"message": "NeuroFlow API is running"}