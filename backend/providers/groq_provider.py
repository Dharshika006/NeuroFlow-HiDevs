import os

from groq import AsyncGroq

from dotenv import load_dotenv

load_dotenv()


class GroqProvider:

    def __init__(self):

        self.client = AsyncGroq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    async def stream(

        self,

        prompt

    ):

        stream = await self.client.chat.completions.create(

            model="llama3-8b-8192",

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,

            stream=True
        )

        async for chunk in stream:

            delta = (
                chunk.choices[0]
                .delta
                .content
            )

            if delta:

                yield delta