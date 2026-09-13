from typing import Any

from services.trusted_user_context import (
    build_trusted_user_context
)


# ============================================================
# USER ANSWER CAPTURE
# ============================================================

def capture_user_answers(
    user_answers: dict[str, Any]
):
    """
    Capture explicit answers supplied by the user.

    This function is the intended boundary between:
    
        USER INPUT
              ↓
        TRUSTED USER CONTEXT

    Important:

        AI-generated workflow data must not be passed here
        to obtain user_confirmed provenance.
    """

    # --------------------------------------------------------
    # Validate input type
    # --------------------------------------------------------

    if not isinstance(user_answers, dict):

        return {
            "valid": False,
            "errors": [
                "User answers must be a dictionary."
            ],
            "trusted_context": {
                "confirmed_fields": {}
            }
        }

    # --------------------------------------------------------
    # Build trusted context
    # --------------------------------------------------------

    context_result = build_trusted_user_context(
        user_answers
    )

    if not context_result["valid"]:

        return {
            "valid": False,
            "errors": context_result["errors"],
            "trusted_context": {
                "confirmed_fields": {}
            }
        }

    # --------------------------------------------------------
    # Return trusted context
    # --------------------------------------------------------

    return {
        "valid": True,
        "errors": [],
        "trusted_context": context_result
    }