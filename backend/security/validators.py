import re


def validate_pipeline_name(
    name: str
):

    return len(name) <= 100


def validate_query(
    query: str
):

    return len(query) <= 5000


def validate_url(
    url: str
):

    return bool(
        re.match(
            r"^https?://",
            url
        )
    )