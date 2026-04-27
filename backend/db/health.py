import redis.asyncio as redis
import httpx
from config import settings
from db.pool import get_pool


async def check_postgres():
    try:
        pool = get_pool()
        if pool is None:
            return False

        async with pool.acquire() as conn:
            await conn.execute("SELECT 1")

        return True
    except Exception as e:
        print(f"Postgres health error: {e}")
        return False


async def check_redis():
    try:
        r = redis.from_url(settings.redis_url)
        await r.ping()
        return True
    except Exception as e:
        print(f"Redis health error: {e}")
        return False


async def check_mlflow():
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(settings.mlflow_url)
            return res.status_code == 200
    except Exception as e:
        print(f"MLflow health error: {e}")
        return False