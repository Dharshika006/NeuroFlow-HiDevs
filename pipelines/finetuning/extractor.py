import os
import json
import uuid
import asyncpg

from dotenv import load_dotenv

from pipelines.finetuning.validator import (
    validate_pair
)

load_dotenv()


class TrainingExtractor:

    # =====================================================
    # DB CONNECTION
    # =====================================================

    async def connect(self):

        return await asyncpg.connect(
            os.getenv("POSTGRES_URL")
        )

    # =====================================================
    # STANDARD SFT EXTRACTION
    # =====================================================

    async def extract(self):

        conn = await self.connect()

        rows = await conn.fetch(
            """
            SELECT *

            FROM training_pairs

            WHERE score >= 0.82
            """
        )

        validated = []

        for row in rows:

            pair = {

                "query": row["query"],

                "answer": row["answer"],

                "context": row["context"],

                "score": row["score"]
            }

            # =========================
            # VALIDATION
            # =========================

            if validate_pair(pair):

                validated.append(pair)

        # =========================
        # JOB ID + OUTPUT FILE
        # =========================

        job_id = str(uuid.uuid4())

        os.makedirs(
            "training_data",
            exist_ok=True
        )

        path = f"training_data/{job_id}.jsonl"

        # =========================
        # WRITE JSONL
        # =========================

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            for pair in validated:

                item = {

                    "messages": [

                        {
                            "role": "system",

                            "content":
                            "You are a precise research assistant."
                        },

                        {
                            "role": "user",

                            "content":
                            f"[Context]\n{pair['context']}\n\n[Question]\n{pair['query']}"
                        },

                        {
                            "role": "assistant",

                            "content":
                            pair["answer"]
                        }
                    ]
                }

                f.write(
                    json.dumps(item) + "\n"
                )

        await conn.close()

        return {

            "job_id": job_id,

            "path": path,

            "pairs": validated
        }

    # =====================================================
    # DPO EXTRACTION
    # =====================================================

    async def extract_dpo_pairs(self):

        conn = await self.connect()

        rows = await conn.fetch(
            """
            SELECT *

            FROM training_pairs
            """
        )

        dpo_pairs = []

        for row in rows:

            if row["score"] >= 0.8:

                dpo_pairs.append({

                    "prompt": row["query"],

                    "chosen": row["answer"],

                    "rejected":
                    "Insufficient answer."
                })

        await conn.close()

        return dpo_pairs