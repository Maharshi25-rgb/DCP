from services.input_security import validate_user_input

from services.prompt_injection_detector import (
    detect_prompt_injection
)

from services.security_risk_classifier import (
    classify_security_risk
)


def check_input_security(user_request: str):
    """
    Central security gateway for DCP user input.

    Security flow:

        Input Validation
              ↓
        Injection Detection
              ↓
        Risk Classification
              ↓
        Security Decision
    """

    # ========================================================
    # STAGE 1 — INPUT VALIDATION
    # ========================================================

    input_validation = validate_user_input(
        user_request
    )

    if not input_validation["valid"]:

        return {
            "secure": False,
            "decision": "block",
            "stage": "input_validation",
            "reason": "invalid_input",
            "risk_level": "low",
            "errors": input_validation["errors"],
            "injection_detected": False,
            "categories": []
        }

    # ========================================================
    # STAGE 2 — PROMPT INJECTION DETECTION
    # ========================================================

    injection_result = detect_prompt_injection(
        user_request
    )

    # ========================================================
    # STAGE 3 — RISK CLASSIFICATION
    # ========================================================

    risk_result = classify_security_risk(
        injection_detected=injection_result["detected"],
        categories=injection_result["categories"]
    )

    # ========================================================
    # STAGE 4 — SECURITY DECISION
    # ========================================================

    if risk_result["action"] == "block":

        return {
            "secure": False,
            "decision": "block",
            "stage": "security_policy",
            "reason": "prompt_injection_detected",
            "risk_level": risk_result["risk_level"],
            "errors": [],
            "injection_detected": injection_result["detected"],
            "categories": injection_result["categories"],
            "risk_reasons": risk_result["reasons"]
        }

    # ========================================================
    # ALLOW
    # ========================================================

    return {
        "secure": True,
        "decision": "allow",
        "stage": "security_policy",
        "reason": "input_allowed",
        "risk_level": risk_result["risk_level"],
        "errors": [],
        "injection_detected": False,
        "categories": [],
        "risk_reasons": []
    }