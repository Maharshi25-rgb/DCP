import re


# ============================================================
# PROMPT INJECTION PATTERNS
# ============================================================

INJECTION_PATTERNS = {

    # --------------------------------------------------------
    # Instruction Override
    # --------------------------------------------------------

    "instruction_override": [

        r"\bignore\s+(all\s+)?(previous|prior|earlier)\s+instructions\b",

        r"\bdisregard\s+(all\s+)?(previous|prior|earlier)\s+instructions\b",

        r"\bforget\s+(all\s+)?(previous|prior|earlier)\s+instructions\b",

        r"\boverride\s+(the\s+)?(previous|prior|system|developer)\s+instructions\b",

        r"\bdo\s+not\s+follow\s+(the\s+)?(previous|prior|system|developer)\s+instructions\b",

        r"\bignore\s+(the\s+)?(developer|system)\s+instructions\b",

        r"\bdisregard\s+(the\s+)?(developer|system)\s+instructions\b",

        r"\bforget\s+(the\s+)?(developer|system)\s+instructions\b",
    ],


    # --------------------------------------------------------
    # System / Developer Prompt Extraction
    # --------------------------------------------------------

    "system_prompt_extraction": [

        r"\b(reveal|show|print|display|provide|give|tell\s+me)\b"
        r".{0,100}"
        r"\b(system|developer)\s+(prompt|instructions)\b",

        r"\bwhat\s+(is|are)\s+(your|the)\s+(system|developer)"
        r"\s+(prompt|instructions)\b",

        r"\bshow\s+me\s+your\s+(system|developer)"
        r"\s+(prompt|instructions)\b",
    ],


    # --------------------------------------------------------
    # Role Manipulation
    # --------------------------------------------------------

    "role_manipulation": [

        r"\byou\s+are\s+now\s+(a|an|the)\b",

        r"\bact\s+as\s+(a|an|the)?\s*system\b",

        r"\bpretend\s+to\s+be\s+(a|an|the)?\s*system\b",

        r"\bact\s+as\s+the\s+system\s+administrator\b",
    ],


    # --------------------------------------------------------
    # Internal Information Extraction
    # --------------------------------------------------------

    "internal_information_extraction": [

        r"\breveal\s+(your\s+)?internal\s+(instructions|rules|configuration)\b",

        r"\bshow\s+(your\s+)?internal\s+(instructions|rules|configuration)\b",

        r"\bprovide\s+(your\s+)?internal\s+(instructions|rules|configuration)\b",

        r"\bexpose\s+(your\s+)?internal\s+(instructions|rules|configuration)\b",
    ],
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize whitespace in a string.

    Example:

        Ignore     previous
        instructions

    becomes:

        Ignore previous instructions
    """

    return re.sub(
        r"\s+",
        " ",
        text.strip()
    )


# ============================================================
# PROMPT INJECTION DETECTOR
# ============================================================

def detect_prompt_injection(
    user_request: str
):
    """
    Detect known prompt-injection patterns.

    The detector expects a string.

    Non-string input is handled safely and does not
    cause the detector to crash.

    Returns:

        {
            "detected": bool,
            "categories": [...],
            "matches": [...]
        }
    """

    # ========================================================
    # INPUT TYPE CHECK
    # ========================================================

    if not isinstance(user_request, str):

        return {
            "detected": False,
            "categories": [],
            "matches": []
        }


    # ========================================================
    # NORMALIZE INPUT
    # ========================================================

    normalized_text = normalize_text(
        user_request
    )

    detected_categories = []
    matches = []


    # ========================================================
    # CHECK SECURITY CATEGORIES
    # ========================================================

    for category, patterns in INJECTION_PATTERNS.items():

        category_detected = False

        for pattern in patterns:

            match = re.search(
                pattern,
                normalized_text,
                flags=re.IGNORECASE
            )

            if match:

                category_detected = True

                matches.append({
                    "category": category,
                    "match": match.group(0)
                })

                # One matching pattern is enough
                # to mark this category.
                break


        if category_detected:

            detected_categories.append(
                category
            )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {
        "detected": bool(
            detected_categories
        ),

        "categories": detected_categories,

        "matches": matches
    }