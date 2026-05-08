import os
import asyncio
from google import genai

class GeminiProvider:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise Exception("GEMINI_API_KEY not set")

        self.client = genai.Client(api_key=api_key)

    async def stream(self, messages, model="gemini-2.0-flash"):
        prompt = self._format(messages)

        retries = 3

        for attempt in range(retries):
            try:
                stream = self.client.models.generate_content_stream(
                    model=model,
                    contents=prompt
                )

                for chunk in stream:
                    if chunk.text:
                        yield chunk.text

                return

            except Exception as e:
                print(f"[Gemini Retry] {e}")
                await asyncio.sleep(2 ** attempt)

        raise Exception("Gemini failed after retries")

    async def embed(self, texts):
        # Dummy embedding
        return [[0.2] * 768 for _ in texts]

    def _format(self, messages):
        """
        Accepts:
        [{"role": "user", "content": "hi"}]
        """
        formatted = []

        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            formatted.append(f"{role}: {content}")

        return "\n".join(formatted)