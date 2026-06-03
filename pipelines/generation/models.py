from dataclasses import dataclass


@dataclass
class Citation:

    reference: str

    chunk_id: str

    document_name: str

    page_number: int | None

    content_preview: str

    invalid_citation: bool = False