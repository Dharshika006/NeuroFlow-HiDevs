from typing import List

from pipelines.ingestion.models import ExtractedPage


def fixed_size_chunk(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunks.append(text[i:i + chunk_size])

    return chunks


def semantic_chunk(text):

    return fixed_size_chunk(text, 700)


def hierarchical_chunk(text):

    return fixed_size_chunk(text, 1000)


def select_strategy(page):

    if page.content_type == "table":
        return fixed_size_chunk

    if "heading" in page.metadata:
        return hierarchical_chunk

    return semantic_chunk


def chunk_pages(
    pages: List[ExtractedPage]
):

    all_chunks = []

    for page in pages:

        strategy = select_strategy(page)

        chunks = strategy(page.content)

        for chunk in chunks:

            all_chunks.append({
                "content": chunk,
                "metadata": page.metadata
            })

    return all_chunks


