import httpx
import trafilatura

from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

from pipelines.ingestion.models import ExtractedPage


async def extract_url(url: str):

    parsed = urlparse(url)

    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    rp = RobotFileParser()

    rp.set_url(robots_url)

    try:
        rp.read()

        allowed = rp.can_fetch("*", url)

    except:
        allowed = True

    if not allowed:
        raise Exception("Blocked by robots.txt")

    async with httpx.AsyncClient() as client:

        response = await client.get(url)

    extracted = trafilatura.extract(
        response.text,
        include_tables=True
    )

    return [
        ExtractedPage(
            page_number=1,
            content=extracted or "",
            content_type="text",
            metadata={
                "source": "url",
                "url": url
            }
        )
    ]
