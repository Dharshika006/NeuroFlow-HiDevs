import pytest
from httpx import AsyncClient

BASE_URL = "http://127.0.0.1:8000"


@pytest.mark.asyncio
async def test_ingest_requires_auth():

    async with AsyncClient() as client:

        response = await client.post(
            f"{BASE_URL}/ingest"
        )

    assert response.status_code in [401,422]