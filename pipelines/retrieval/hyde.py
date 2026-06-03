class HyDEGenerator:

    async def generate(
        self,
        query
    ):

        hypothetical = f"""
This document explains:

{query}

Detailed technical explanation:

{query}

Key concepts, definitions,
and implementation details
related to:

{query}
"""

        return hypothetical.strip()