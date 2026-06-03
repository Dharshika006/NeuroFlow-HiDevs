import os
import asyncio
import asyncpg

from dotenv import load_dotenv

load_dotenv()

from opentelemetry import trace

from evaluation.metrics.faithfulness import (
    evaluate_faithfulness
)

from evaluation.metrics.answer_relevance import (
    evaluate_answer_relevance
)

from evaluation.metrics.context_precision import (
    evaluate_context_precision
)

from evaluation.metrics.context_recall import (
    evaluate_context_recall
)

tracer = trace.get_tracer(__name__)


class EvaluationJudge:

    async def connect(self):

        return await asyncpg.connect(
            os.getenv("POSTGRES_URL")
        )

    async def evaluate(

        self,

        run_id,

        query,

        answer,

        context,

        chunks

    ):

        with tracer.start_as_current_span(
            "evaluation.judge"
        ) as span:

            (
                faithfulness,
                answer_relevance,
                context_precision,
                context_recall

            ) = await asyncio.gather(

                evaluate_faithfulness(
                    query,
                    answer,
                    context
                ),

                evaluate_answer_relevance(
                    query,
                    answer
                ),

                evaluate_context_precision(
                    query,
                    chunks,
                    answer
                ),

                evaluate_context_recall(
                    query,
                    chunks,
                    answer
                )
            )

            overall = (

                0.35 * faithfulness +

                0.30 * answer_relevance +

                0.20 * context_precision +

                0.15 * context_recall
            )

            span.set_attribute(
                "faithfulness",
                faithfulness
            )

            span.set_attribute(
                "answer_relevance",
                answer_relevance
            )

            span.set_attribute(
                "context_precision",
                context_precision
            )

            span.set_attribute(
                "context_recall",
                context_recall
            )

            conn = await self.connect()

            await conn.execute(
                """
                INSERT INTO evaluations (

                    run_id,
                    faithfulness,
                    answer_relevance,
                    context_precision,
                    context_recall,
                    overall_score,
                    metadata

                )

                VALUES (

                    $1,$2,$3,$4,$5,$6,$7
                )
                """,

                run_id,

                faithfulness,

                answer_relevance,

                context_precision,

                context_recall,

                overall,

                {}
            )

            if overall > 0.8:

                await conn.execute(
                    """
                    INSERT INTO training_pairs (

                        run_id,
                        query,
                        answer,
                        context,
                        score

                    )

                    VALUES (

                        $1,$2,$3,$4,$5
                    )
                    """,

                    run_id,
                    query,
                    answer,
                    context,
                    overall
                )

            await conn.close()

            return {

                "faithfulness": faithfulness,

                "answer_relevance": answer_relevance,

                "context_precision": context_precision,

                "context_recall": context_recall,

                "overall_score": overall
            }