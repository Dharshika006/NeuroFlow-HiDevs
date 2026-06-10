import re


INJECTION_PATTERNS = [
    # Matches "ignore" followed by any combination of modifiers and spaces, ending in "instructions"
    r"ignore\s+(?:all\s+|previous\s+|the\s+|your\s+)*instructions",
    r"you are now",
    r"new\s+(?:system\s+)?prompt",
    r"disregard\s+(?:the\s+|all\s+|previous\s+)*",
    r"forget\s+(?:everything|all|previous)",
    r"act as\s+(?:if\s+|a\s+|an\s+)?",
    r"\[\[(system|SYSTEM)\]\]",
    r"<\|system\|>"
]


def detect_prompt_injection(
    text: str
):

    for pattern in INJECTION_PATTERNS:

        if re.search(

            pattern,

            text,

            re.IGNORECASE

        ):

            return {

                "prompt_injection_detected":
                True,

                "pattern":
                pattern
            }

    return {

        "prompt_injection_detected":
        False
    }