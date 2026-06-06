from backend.services.anomaly_detector import (
    is_anomaly
)


class PipelineOptimizer:

    def suggest(
        self,
        metrics
    ):

        suggestions = []

        if metrics.get(
            "context_precision",
            1
        ) < 0.5:

            suggestions.append(
                "Reduce top_k_after_rerank"
            )

        if metrics.get(
            "context_recall",
            1
        ) < 0.5:

            suggestions.append(
                "Increase dense_k"
            )

        if metrics.get(
            "faithfulness",
            1
        ) < 0.6:

            suggestions.append(
                "Reduce generation temperature"
            )

        return suggestions

    def detect_quality_anomaly(
        self,
        scores
    ):

        return is_anomaly(
            scores
        )