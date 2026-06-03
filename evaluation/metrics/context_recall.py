import re


async def evaluate_context_recall(

    query,

    chunks,

    answer

):

    if not chunks:

        return 0.0

    context = " ".join(chunks).lower()

    sentences = re.split(r"[.!?]", answer)

    sentences = [

        s.strip()

        for s in sentences

        if s.strip()
    ]

    if not sentences:

        return 1.0

    attributable = 0

    for sentence in sentences:

        overlap = sum(

            1

            for w in sentence.lower().split()

            if w in context
        )

        if overlap > 3:
            attributable += 1

    return attributable / len(sentences)