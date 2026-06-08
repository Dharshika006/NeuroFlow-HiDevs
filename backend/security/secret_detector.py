import re


PATTERNS = {

    "aws":

    r"AKIA[0-9A-Z]{16}",

    "jwt":

    r"[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",

    "private_key":

    r"-----BEGIN .* PRIVATE KEY-----",

    "api_key":

    r"""['"]?(?:api|secret|token|key|password)['"]?\s*[:=]\s*['"][A-Za-z0-9/+]{20,}['"]"""
}


def redact_secrets(
    text: str
):

    events = []

    for name, pattern in PATTERNS.items():

        if re.search(
            pattern,
            text
        ):

            events.append(
                name
            )

            text = re.sub(

                pattern,

                "[REDACTED]",

                text
            )

    return text, events