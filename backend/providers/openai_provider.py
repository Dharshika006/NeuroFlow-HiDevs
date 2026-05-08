import os
import asyncio
from openai import AsyncOpenAI


class OpenAIProvider:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise Exception("GROQ_API_KEY not set")

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    async def stream(self, messages, model="llama3-8b-8192"):
        retries = 3

        for attempt in range(retries):
            try:
                stream = await self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True
                )

                async for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

                return  # success → exit

            except Exception as e:
                print(f"[Groq Retry] {e}")

                if attempt == retries - 1:
                    raise Exception("Groq failed after retries")

                await asyncio.sleep(2 ** attempt)