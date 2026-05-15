import asyncio
from backend.providers.router import ModelRouter, RoutingCriteria, FallbackChain
from backend.providers.base import ChatMessage


async def test_router():
    router = ModelRouter()

    criteria = RoutingCriteria(
        task_type="rag_generation"
    )

    provider = await router.route(criteria)

    print("Selected model:", provider.model)

    async for token in provider.stream([
        ChatMessage(role="user", content="Say one word")
    ]):
        print(token, end="", flush=True)


async def test_fallback():
    print("\n\nTesting fallback chain:")

    chain = FallbackChain([
        "llama-3.3-70b-versatile",   # may fail
        "llama-3.1-8b-instant"       # safe fallback
    ])

    async for token in chain.stream([
        ChatMessage(role="user", content="Say one word")
    ]):
        print(token, end="", flush=True)


async def main():
    await test_router()
    await test_fallback()


asyncio.run(main())