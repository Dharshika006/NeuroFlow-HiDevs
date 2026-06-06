from statistics import mean, stdev


def is_anomaly(scores: list[float]) -> bool:
    """
    Returns True if the latest score is more than
    2 standard deviations below the rolling mean.
    """

    if len(scores) < 10:
        return False

    try:
        avg = mean(scores)
        std = stdev(scores)

        latest = scores[-1]

        return latest < (avg - 2 * std)

    except Exception:
        return False


def get_anomaly_details(scores: list[float]) -> dict:
    """
    Returns useful anomaly statistics.
    """

    if len(scores) < 10:
        return {
            "anomaly": False,
            "reason": "Not enough data"
        }

    avg = mean(scores)
    std = stdev(scores)
    latest = scores[-1]

    anomaly = latest < (avg - 2 * std)

    return {
        "anomaly": anomaly,
        "mean": round(avg, 4),
        "std": round(std, 4),
        "latest": round(latest, 4),
        "threshold": round(avg - 2 * std, 4)
    }