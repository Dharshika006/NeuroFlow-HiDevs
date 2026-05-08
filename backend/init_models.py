import asyncio
import json
import os
import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

async def main():
    # Establish connection with password from .env
    r = redis.Redis(
        host="localhost", 
        port=6379, 
        password=os.getenv("REDIS_PASSWORD"), 
        decode_responses=True
    )

    # These keys (vision, context_window, estimated_cost) 
    # now perfectly match your router's filtering logic.
    models = [
        {
            "provider": "gemini",
            "model": "gemini-2.0-flash",
            "vision": True,
            "context_window": 1000000,
            "estimated_cost": 0.0001,
            "fine_tuned": False,
            "judge_model": False
        },
        {
            "provider": "groq",
            "model": "llama-3.1-8b-instant",
            "vision": False,
            "context_window": 128000,
            "estimated_cost": 0.0,
            "fine_tuned": False,
            "judge_model": False
        },
        {
            "provider": "gemini",
            "model": "gemini-1.5-pro",
            "vision": True,
            "context_window": 2000000,
            "estimated_cost": 0.01,
            "fine_tuned": False,
            "judge_model": True
        }
    ]

    try:
        await r.set("router:models", json.dumps(models))
        print("✅ Successfully initialized models in Redis.")
        print(f"Verified keys: {list(models[0].keys())}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await r.aclose()

if __name__ == "__main__":
    asyncio.run(main())