import bleach


def sanitize_text(
    text: str
):

    return bleach.clean(
        text,
        tags=[],
        strip=True
    )