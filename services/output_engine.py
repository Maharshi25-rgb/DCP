from typing import Any

from models.generic_workflow import GenericWorkflow

from services.output_validator import (
    validate_ai_output
)

from services.ai_output_checker import (
    check_ai_output
)

from services.output_repair_service import (
    repair_ai_output
)


# ============================================================
# CONFIGURATION
# ============================================================

MAX_AI_REPAIR_ATTEMPTS = 2


# ============================================================
# OUTPUT ENGINE
# ============================================================

def process_ai_output(
    ai_response: Any,
    workflow: GenericWorkflow
):
    """
    Complete DCP AI output processing pipeline.

    Pipeline:

        AI Response
             ↓
        Deterministic Validation
             ↓
        AI Semantic Check
             ↓
          PASS → ACCEPT
             ↓
          FAIL
             ↓
        Repair
             ↓
        Validate Again
             ↓
        Accept OR Controlled Failure

    Security principle:

        The workflow is authoritative.

        Repair may change the AI response, but never the
        workflow itself.
    """

    current_response = ai_response
    repair_attempts = 0

    # ========================================================
    # INITIAL VALIDATION LOOP
    # ========================================================

    while True:

        # ====================================================
        # STAGE 1 — DETERMINISTIC VALIDATION
        # ====================================================

        deterministic_result = validate_ai_output(
            current_response,
            workflow
        )

        if not deterministic_result["valid"]:

            # ------------------------------------------------
            # Repair limit
            # ------------------------------------------------

            if repair_attempts >= MAX_AI_REPAIR_ATTEMPTS:

                return {
                    "status": "failed",
                    "stage": "repair_limit_exceeded",
                    "deterministic_validation":
                        deterministic_result,
                    "ai_check": None,
                    "repair_attempts":
                        repair_attempts,
                    "response": current_response
                }

            # ------------------------------------------------
            # Repair
            # ------------------------------------------------

            repair_result = repair_ai_output(
                current_response,
                workflow,
                deterministic_result
            )

            if not repair_result["success"]:

                return {
                    "status": "failed",
                    "stage": "repair_failed",
                    "deterministic_validation":
                        deterministic_result,
                    "ai_check": None,
                    "repair_attempts":
                        repair_attempts,
                    "repair_error":
                        repair_result["error"],
                    "response": current_response
                }

            repair_attempts += 1

            current_response = (
                repair_result["response"]
            )

            continue

        # ====================================================
        # STAGE 2 — AI SEMANTIC CHECK
        # ====================================================

        ai_check_result = check_ai_output(
            current_response,
            workflow
        )

        if not ai_check_result["valid"]:

            # ------------------------------------------------
            # Repair limit
            # ------------------------------------------------

            if repair_attempts >= MAX_AI_REPAIR_ATTEMPTS:

                return {
                    "status": "failed",
                    "stage": "repair_limit_exceeded",
                    "deterministic_validation":
                        deterministic_result,
                    "ai_check":
                        ai_check_result,
                    "repair_attempts":
                        repair_attempts,
                    "response": current_response
                }

            # ------------------------------------------------
            # Repair
            # ------------------------------------------------

            repair_result = repair_ai_output(
                current_response,
                workflow,
                ai_check_result
            )

            if not repair_result["success"]:

                return {
                    "status": "failed",
                    "stage": "repair_failed",
                    "deterministic_validation":
                        deterministic_result,
                    "ai_check":
                        ai_check_result,
                    "repair_attempts":
                        repair_attempts,
                    "repair_error":
                        repair_result["error"],
                    "response": current_response
                }

            repair_attempts += 1

            current_response = (
                repair_result["response"]
            )

            continue

        # ====================================================
        # STAGE 3 — ACCEPT
        # ====================================================

        return {
            "status": "accepted",
            "stage": "output_validation_complete",
            "deterministic_validation":
                deterministic_result,
            "ai_check":
                ai_check_result,
            "repair_attempts":
                repair_attempts,
            "response":
                current_response
        }