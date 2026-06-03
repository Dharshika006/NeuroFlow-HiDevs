import re

from pipelines.generation.models import Citation


class CitationParser:

    async def parse(

        self,

        response_text,

        chunks

    ):

        citations = []

        matches = re.findall(
            r"\[Source\s+(\d+)\]",
            response_text
        )

        seen = set()

        for match in matches:

            if match in seen:
                continue

            seen.add(match)

            index = int(match) - 1

            # hallucinated citation
            if index >= len(chunks):

                citations.append(

                    Citation(
                        reference=f"Source {match}",
                        chunk_id="invalid",
                        document_name="invalid",
                        page_number=None,
                        content_preview="",
                        invalid_citation=True
                    )
                )

                continue

            chunk = chunks[index]

            preview = chunk.content[:100]

            citations.append(

                Citation(
                    reference=f"Source {match}",
                    chunk_id=chunk.chunk_id,
                    document_name=chunk.metadata.get(
                        "document",
                        "unknown"
                    ),
                    page_number=chunk.metadata.get(
                        "page"
                    ),
                    content_preview=preview,
                    invalid_citation=False
                )
            )

        return citations