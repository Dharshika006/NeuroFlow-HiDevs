import re


EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

PHONE_REGEX = r"\+?\d[\d -]{8,}\d"


def contains_pii(text):

    if re.search(EMAIL_REGEX, text):
        return True

    if re.search(PHONE_REGEX, text):
        return True

    return False


def validate_pair(pair):

    answer = pair["answer"]

    if len(answer.split()) < 50:
        return False

    if len(answer.split()) > 2000:
        return False

    if "[Source" not in answer:
        return False

    if contains_pii(pair["query"]):
        return False

    return True