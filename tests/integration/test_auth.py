import pytest
from httpx import AsyncClient

BASE_URL = "http://127.0.0.1:8000"


@pytest.mark.asyncio
async def test_missing_token():

    async with AsyncClient() as client:

        response = await client.post(

            f"{BASE_URL}/query",

            json={
                "query": "hello"
            }
        )

    assert response.status_code == 401