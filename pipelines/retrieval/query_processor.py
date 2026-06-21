import re


class QueryProcessor:

    async def expand_query(
        self,
        query: str
    ):

        expansions = [
            query,
            f"Explain {query}",
            f"Detailed information about {query}"
        ]

        return expansions

    async def extract_metadata_filters(
        self,
        query: str
    ):

        filters: dict[str, object] = {}

        year_match = re.search(
            r"\b(20\d{2})\b",
            query
        )

        if year_match:

            filters["year"] = int(
                year_match.group(1)
            )

        if "climate" in query.lower():

            filters["topic"] = "climate"

        return filters

    async def classify_query(
        self,
        query: str
    ):

        q = query.lower()

        if "how" in q:
            return "procedural"

        if "compare" in q:
            return "comparative"

        if "why" in q:
            return "analytical"

        return "factual"