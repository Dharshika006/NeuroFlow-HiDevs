import asyncio
from providers.gemini_provider import GeminiProvider


async def main():
    provider = GeminiProvider()

    print("=== Streaming Test ===")

    async for token in provider.stream([
        {"role": "user", "content": "Say hello in a cool way"}
    ]):
        print(token, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())