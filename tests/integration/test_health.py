import pytest
from httpx import AsyncClient

BASE_URL = "http://127.0.0.1:8000"


@pytest.mark.asyncio
async def test_health():

    async with AsyncClient() as client:

        response = await client.get(
            f"{BASE_URL}/health"
        )

    assert response.status_code == 200