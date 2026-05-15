import asyncio
import os
from dotenv import load_dotenv

# Import the client and the criteria dataclass
from backend.providers.client1 import NeuroFlowClient
from backend.providers.router import RoutingCriteria

load_dotenv()

async def main():
    # 1. Initialize the NeuroFlow client
    # This internally sets up the Router and Redis connection
    client = NeuroFlowClient()

    print("=== STARTING CHAT TEST ===")
    
    # 2. Define your message
    messages = [
        {"role": "user", "content": "Hello! Can you tell me which model you are?"}
    ]

    # 3. Call the chat method
    # Note: If you want to force a specific type of model (e.g., Vision),
    # you would usually pass that logic inside client1.py or as an argument here.
    try:
        async for token in client.chat(messages):
            # print(token) usually yields small strings (chunks)
            print(token, end="", flush=True)
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")

    print("\n\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    # Ensure the event loop runs the async main function
    asyncio.run(main())