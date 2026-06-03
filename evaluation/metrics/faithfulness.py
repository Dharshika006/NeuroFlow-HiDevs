import re


async def evaluate_faithfulness(

    query,

    answer,

    context

):

    if not context.strip():

        return 0.0

    claims = re.split(r"[.!?]", answer)

    claims = [

        c.strip()

        for c in claims

        if c.strip()
    ]

    if not claims:

        return 1.0

    supported = 0

    for claim in claims:

        words = claim.lower().split()

        overlap = sum(

            1

            for w in words

            if w in context.lower()
        )

        ratio = overlap / max(len(words), 1)

        if ratio > 0.7:

            supported += 1

        elif ratio > 0.4:

            supported += 0.5

    return min(
        supported / len(claims),
        1.0
    )