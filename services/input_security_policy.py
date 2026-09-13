from services.prompt_injection_detector import (
    detect_prompt_injection
)


# =========================================
# SECURITY ACTIONS
# =========================================

ALLOW = "allow"
BLOCK = "block"


def evaluate_input_security(
    user_request: str
):
    """
    Decide what DCP should do with a user request
    after applying input-boundary and prompt-injection checks.

    Detection and enforcement are intentionally separated.
    """

    # =========================================
    # BASIC INPUT VALIDATION
    # =========================================

    if not isinstance(user_request, str):

        return {
            "decision": BLOCK,
            "reason": "invalid_input_type",
            "injection_detected": False,
            "categories": []
        }

    if not user_request.strip():

        return {
            "decision": BLOCK,
            "reason": "empty_input",
            "injection_detected": False,
            "categories": []
        }

    # =========================================
    # PROMPT INJECTION DETECTION
    # =========================================

    injection_result = detect_prompt_injection(
        user_request
    )

    if injection_result["detected"]:

        return {
            "decision": BLOCK,
            "reason": "prompt_injection_detected",
            "injection_detected": True,
            "categories": injection_result[
                "categories"
            ]
        }

    # =========================================
    # ALLOW
    # =========================================

    return {
        "decision": ALLOW,
        "reason": "input_allowed",
        "injection_detected": False,
        "categories": []
    }