import asyncio
import asyncpg
from config import settings

async def main():
    print("🚀 Worker started")

    try:
        conn = await asyncpg.connect(settings.postgres_url)
        print("✅ Connected to Postgres")

        while True:
            print("⏳ Worker running...")
            await asyncio.sleep(10)

    except Exception as e:
        print(f"❌ Worker error: {e}")

if __name__ == "__main__":
    asyncio.run(main())