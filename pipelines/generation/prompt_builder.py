class PromptBuilder:

    BASE_PROMPT = """
You are a precise research assistant.

Answer the user's question
using ONLY the provided context.

If the context does not contain
enough information to answer fully,
say so explicitly.

For every factual claim,
include citations in the format [Source N].

Do not introduce information
not present in the context.
"""

    TYPE_PROMPTS = {

        "factual":
        """
Provide a direct concise answer.
If multiple sources agree,
cite all of them.
""",

        "analytical":
        """
Analyze and synthesize
across provided sources.

Identify agreements
and contradictions.
""",

        "comparative":
        """
Organize your response
as structured comparison.

Use table if appropriate.
""",

        "procedural":
        """
Provide numbered steps.

Each step must be cited.
"""
    }

    async def build(

        self,

        query,

        context,

        query_type="factual"

    ):

        extra = self.TYPE_PROMPTS.get(
            query_type,
            ""
        )

        prompt = f"""
{self.BASE_PROMPT}

{extra}

<context>

{context}

</context>

Question:
{query}
"""

        return prompt.strip()