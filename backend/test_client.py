import asyncio
import os
import redis
from providers.client import NeuroFlowClient
from providers.base import ChatMessage
from providers.router import RoutingCriteria
from dotenv import load_dotenv
load_dotenv()


async def main():
    client = NeuroFlowClient.get_instance()

    print("Streaming response:\n")

    async for token in client.chat(
        [ChatMessage(role="user", content="Say one word")],
        RoutingCriteria(task_type="rag_generation")
    ):
        print(token, end="", flush=True)

    print("\n\nEmbedding test:")

    emb = await client.embed(["hello world"])
    print(len(emb[0]))


asyncio.run(main())
def get_redis():
    return redis.Redis(
        host="localhost",
        port=6379,
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )