import tiktoken


class ContextAssembler:

    def __init__(self):

        self.encoder = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text):

        return len(self.encoder.encode(text))

    async def assemble(
        self,
        chunks,
        token_budget=4000
    ):

        context = []

        used_chunks = []

        total_tokens = 0

        sources = []

        for i, chunk in enumerate(chunks):

            formatted = f"""
[Source {i+1}]
{chunk.content}
"""

            tokens = self.count_tokens(formatted)

            if total_tokens + tokens > token_budget:
                break

            context.append(formatted)

            used_chunks.append(chunk.chunk_id)

            sources.append(chunk.metadata)

            total_tokens += tokens

        return {
            "context": "\n".join(context),
            "chunks_used": used_chunks,
            "total_tokens": total_tokens,
            "sources": sources
        }