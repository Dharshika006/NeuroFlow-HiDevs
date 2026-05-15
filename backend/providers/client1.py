import time
import os
import redis.asyncio as redis
from dotenv import load_dotenv

# OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# Internal Imports
from backend.providers.router import ModelRouter, RoutingCriteria
from backend.providers.gemini_provider import GeminiProvider
from backend.providers.openai_provider import OpenAIProvider

load_dotenv()

# Trace setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

def get_redis():
    return redis.Redis(
        host="localhost",
        port=6379,
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )

class NeuroFlowClient:
    def __init__(self):
        self.redis = get_redis()
        self.router = ModelRouter()
        
        # Provider Mapping
        self.providers = {
            "gemini": GeminiProvider(),
            "openai": OpenAIProvider(), # Standard OpenAI
            "groq": OpenAIProvider(),   # Groq using OpenAI-compatible SDK
        }

    async def chat(self, messages, criteria=None):
        """
        Primary chat method with automatic fallback to Groq.
        """
        if criteria is None:
            criteria = RoutingCriteria()

        # 1. ROUTE TO PRIMARY MODEL
        model_config = await self.router.route(criteria)
        provider_name = model_config["provider"]
        model_name = model_config["model"]
        
        provider = self.providers.get(provider_name)
        start_time = time.time()

        with tracer.start_as_current_span("chat_session") as span:
            span.set_attribute("primary_model", model_name)

            try:
                # Attempt Primary Provider
                async for token in provider.stream(messages, model=model_name):
                    yield token
                
                # If successful, log metrics
                await self._log_metrics(model_name, model_config.get("estimated_cost", 0), start_time)

            except Exception as e:
                # 2. FALLBACK LOGIC
                print(f"\n[Error] {e}")
                print("[Fallback] Switching to Groq...\n")
                
                span.record_exception(e)
                span.add_event("fallback_triggered")

                fallback_provider = self.providers["groq"]
                fallback_model = "llama-3.1-8b-instant"

                try:
                    async for token in fallback_provider.stream(messages, model=fallback_model):
                        yield token
                    
                    # Log fallback metrics
                    await self._log_metrics(fallback_model, 0.0, start_time)
                
                except Exception as fallback_err:
                    print(f"Critical Failure: Fallback also failed: {fallback_err}")
                    raise fallback_err

    async def _log_metrics(self, model_name, cost, start_time):
        """Helper to record performance in Redis."""
        latency_ms = (time.time() - start_time) * 1000
        await self.redis.incr(f"metrics:model:{model_name}:calls")
        await self.redis.incrbyfloat(f"metrics:model:{model_name}:cost_usd", cost)
        # Optional: Store latency in a list for averaging
        await self.redis.lpush(f"metrics:model:{model_name}:latency", latency_ms)

    async def embed(self, texts):
        return await self.providers["openai"].embed(texts)