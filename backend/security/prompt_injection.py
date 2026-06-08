import re


INJECTION_PATTERNS = [

    r"ignore (all |previous |the |your )?instructions",

    r"you are now",

    r"new (system |)prompt",

    r"disregard (the |all |previous )",

    r"forget (everything|all|previous)",

    r"act as (if |a |an )",

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