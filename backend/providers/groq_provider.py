import os
import asyncio

from groq import AsyncGroq

from dotenv import load_dotenv

from backend.resilience.circuit_breaker import (
    CircuitBreaker
)

from backend.resilience.timeout_manager import (
    TimeoutManager
)

load_dotenv()


class GroqProvider:

    def __init__(self):

        self.client = AsyncGroq(
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

        self.circuit_breaker = CircuitBreaker(
            "groq"
        )

        self.timeout_manager = TimeoutManager()

    async def stream(

        self,

        prompt

    ):

        retries = 3

        for attempt in range(retries):

            try:

                async with self.circuit_breaker.protect():

                    stream = await self.timeout_manager.run(

                        self.client.chat.completions.create(

                            model="llama3-8b-8192",

                            messages=[

                                {
                                    "role": "user",

                                    "content": prompt
                                }
                            ],

                            temperature=0.2,

                            stream=True
                        ),

                        "chat_completion"
                    )

                    async for chunk in stream:

                        delta = (

                            chunk.choices[0]
                            .delta
                            .content
                        )

                        if delta:

                            yield delta

                    return

            except Exception as e:

                print(
                    f"[Groq Retry] {e}"
                )

                if attempt == retries - 1:

                    raise Exception(
                        "Groq failed after retries"
                    )

                await asyncio.sleep(
                    2 ** attempt
                )