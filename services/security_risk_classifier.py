from typing import Literal


RiskLevel = Literal[
    "low",
    "medium",
    "high",
    "critical"
]


# ============================================================
# RISK MAPPING
# ============================================================

CATEGORY_RISK_MAP = {

    # Suspicious instruction manipulation
    "instruction_override": "medium",

    # Attempt to manipulate the AI's role
    "role_manipulation": "medium",

    # Attempt to obtain system/developer instructions
    "system_prompt_extraction": "high",

    # Attempt to obtain internal DCP information
    "internal_information_extraction": "high",

}


# ============================================================
# CLASSIFY SECURITY RISK
# ============================================================

def classify_security_risk(
    injection_detected: bool,
    categories: list[str]
):
    """
    Classify the security risk of a user request
    based on prompt-injection detector results.
    """

    # --------------------------------------------------------
    # No injection detected
    # --------------------------------------------------------

    if not injection_detected:

        return {
            "risk_level": "low",
            "action": "allow",
            "reasons": []
        }


    # --------------------------------------------------------
    # Determine highest risk
    # --------------------------------------------------------

    risk_priority = {
        "low": 0,
        "medium": 1,
        "high": 2,
        "critical": 3
    }

    highest_risk = "low"
    reasons = []

    for category in categories:

        risk = CATEGORY_RISK_MAP.get(
            category,
            "high"
        )

        reasons.append({
            "category": category,
            "risk_level": risk
        })

        if risk_priority[risk] > risk_priority[highest_risk]:

            highest_risk = risk


    # --------------------------------------------------------
    # Determine action
    # --------------------------------------------------------

    if highest_risk == "low":

        action = "allow"

    elif highest_risk == "medium":

        action = "block"

    elif highest_risk == "high":

        action = "block"

    else:

        action = "block"


    return {
        "risk_level": highest_risk,
        "action": action,
        "reasons": reasons
    }