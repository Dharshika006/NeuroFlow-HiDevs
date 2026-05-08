import json
import os
import redis.asyncio as redis
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional

load_dotenv()

# =========================
# ROUTING CRITERIA
# =========================
@dataclass
class RoutingCriteria:
    task_type: str = "rag_generation"
    max_cost_per_call: Optional[float] = None
    require_vision: bool = False
    require_long_context: bool = False
    latency_budget_ms: Optional[int] = None
    prefer_fine_tuned: bool = False

# =========================
# REDIS CLIENT
# =========================
def get_redis():
    return redis.Redis(
        host="localhost",
        port=6379,
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )

# =========================
# MODEL ROUTER
# =========================
class ModelRouter:
    def __init__(self):
        self.redis = get_redis()

    async def _load_models(self):
        """Helper to fetch and parse models from Redis."""
        data = await self.redis.get("router:models")
        if not data:
            raise Exception("No models found in Redis. Please run init_models.py first.")
        return json.loads(data)

    async def route(self, criteria: RoutingCriteria):
        # 1. Load data using your new helper
        models = await self._load_models()

        # 2. Vision routing
        if criteria.require_vision:
            models = [m for m in models if m.get("vision")]

        # 3. Long context routing 
        # (Matched to use 'context' key from your init_models.py)
        if criteria.require_long_context:
            models = [m for m in models if m.get("context", 0) > 100000]

        # 4. Fine tuned routing
        if criteria.prefer_fine_tuned:
            fine_tuned = [
                m for m in models
                if m.get("fine_tuned")
                and m.get("task_type") == criteria.task_type
            ]
            if fine_tuned:
                models = fine_tuned

        # 5. Evaluation routing
        if criteria.task_type == "evaluation":
            models = [
                m for m in models
                if m.get("judge_model", False)
            ]

        # 6. Cost filtering 
        # (Matched to use 'cost' key from your init_models.py)
        if criteria.max_cost_per_call is not None:
            models = [
                m for m in models
                if m.get("cost", 0) <= criteria.max_cost_per_call
            ]

        # 7. Final Safety Check
        if not models:
            # If filters are too strict, fallback to all models rather than crashing
            print("[Router] Warning: No models matched criteria. Using defaults.")
            models = await self._load_models()

        # 8. Cheapest model wins
        # Using .get("cost") to match your Redis schema
        models.sort(key=lambda x: x.get("cost", 999))

        selected = models[0]
        print(f"[Router] Selected: {selected['provider']} | {selected['model']}")

        return selected