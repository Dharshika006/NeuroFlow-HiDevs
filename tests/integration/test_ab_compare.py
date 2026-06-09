import pytest
from httpx import AsyncClient

BASE_URL = "http://127.0.0.1:8000"


@pytest.mark.asyncio
async def test_compare_endpoint_exists():

    async with AsyncClient(
        timeout=30.0
    ) as client:

        response = await client.get(
            f"{BASE_URL}/docs"
        )

    assert response.status_code == 200