import time
import os
import redis.asyncio as redis
from typing import List
from backend.providers.router import ModelRouter, RoutingCriteria
from backend.providers.base import ChatMessage
from backend.providers.redis_client import RedisClient

# ✅ add providers
from backend.providers.openai_provider import OpenAIProvider   # (your groq here)
from backend.providers.gemini_provider import GeminiProvider

# ✅ OpenTelemetry
from opentelemetry import trace

from dotenv import load_dotenv

load_dotenv()
tracer = trace.get_tracer(__name__)


class NeuroFlowClient:

    _instance = None

    def __init__(self):
        self.router = ModelRouter()
        self.redis = RedisClient.get_client()

        # ✅ provider registry
        self.providers = {
            "openai": OpenAIProvider(),   # groq-compatible
            "gemini": GeminiProvider()
        }

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = NeuroFlowClient()
        return cls._instance

    # =========================
    # CHAT (streaming)
    # =========================
    async def chat(self, messages: List[ChatMessage], criteria: RoutingCriteria):

        model_config = await self.router.route(criteria)

        provider_name = model_config["provider"]
        model_name = model_config["model"]

        provider = self.providers[provider_name]

        start_time = time.time()
        output = ""

        with tracer.start_as_current_span("llm_call") as span:

            try:
                async for token in provider.stream(messages, model=model_name):
                    output += token
                    yield token

            except Exception:
                print("[Fallback] Switching provider...")

                # fallback to gemini
                provider = self.providers["gemini"]
                model_name = "gemini-1.5-flash"

                async for token in provider.stream(messages, model=model_name):
                    output += token
                    yield token

            latency_ms = (time.time() - start_time) * 1000

            # simple token estimate
            input_tokens = sum(len(m.content) for m in messages if isinstance(m.content, str))
            output_tokens = len(output)

            cost = (
                input_tokens * provider.cost_per_input_token +
                output_tokens * provider.cost_per_output_token
            )

            # ✅ metrics
            await self._update_metrics(model_name, cost)

            # ✅ telemetry attributes
            span.set_attribute("model", model_name)
            span.set_attribute("input_tokens", input_tokens)
            span.set_attribute("output_tokens", output_tokens)
            span.set_attribute("cost_usd", cost)
            span.set_attribute("latency_ms", latency_ms)

        print(f"\n[METRICS] model={model_name} latency={latency_ms:.2f}ms cost=${cost:.6f}")

    # =========================
    # EMBEDDING
    # =========================
    async def embed(self, texts: List[str]):
        model_config = await self.router.route(
            RoutingCriteria(task_type="embedding")
        )

        provider = self.providers[model_config["provider"]]

        embeddings = await provider.embed(texts)

        await self._update_metrics(model_config["model"], 0)

        return embeddings

    # =========================
    # METRICS TRACKING (Redis)
    # =========================
    async def _update_metrics(self, model_name: str, cost: float):
        await self.redis.incr(f"metrics:model:{model_name}:calls")
        await self.redis.incrbyfloat(f"metrics:model:{model_name}:cost_usd", cost)

def get_redis():
    return redis.Redis(
        host="localhost",
        port=6379,
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )