import asyncpg
from config import settings

_pool = None


async def init_pool():
    global _pool
    _pool = await asyncpg.create_pool(dsn=settings.postgres_url)


async def close_pool():
    global _pool
    if _pool:
        await _pool.close()


def get_pool():
    return _pool