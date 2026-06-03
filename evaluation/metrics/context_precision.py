async def evaluate_context_precision(

    query,

    chunks,

    answer

):

    if not chunks:

        return 0.0

    total = 0
    weights = 0

    for i, chunk in enumerate(chunks, start=1):

        weight = 1 / i

        useful = 0

        overlap = sum(

            1

            for word in answer.lower().split()

            if word in chunk.lower()
        )

        if overlap > 3:
            useful = 1

        total += useful * weight

        weights += weight

    return total / weights