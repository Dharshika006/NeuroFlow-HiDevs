import pandas as pd

from pipelines.ingestion.models import ExtractedPage


async def extract_csv(file_path: str):

    df = pd.read_csv(file_path)

    pages = []

    if len(df) < 1000:

        content = df.to_markdown()

    else:

        content = f"""
Columns: {list(df.columns)}

Shape: {df.shape}

Summary:
{df.describe(include='all').to_string()}
"""

    pages.append(
        ExtractedPage(
            page_number=1,
            content=content,
            content_type="table",
            metadata={"source": "csv"}
        )
    )

    return pages



