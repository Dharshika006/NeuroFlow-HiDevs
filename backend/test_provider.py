import asyncio
from providers.openai_provider import OpenAIProvider
from providers.base import ChatMessage


async def main():
    provider = OpenAIProvider()

    print("Embedding test:")
    emb = await provider.embed(["hello world"])
    print(len(emb[0]))

    print("\nStreaming test:")

    async for token in provider.stream([
        ChatMessage(role="user", content="Say one word only")
    ]):
        print(token, end="", flush=True)


asyncio.run(main())