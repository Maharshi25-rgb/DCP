from models.generic_workflow import GenericWorkflow

from services.input_security_service import (
    check_input_security
)

from services.workflow_normalizer import (
    normalize_workflow
)

from services.workflow_validator import (
    validate_workflow
)

from services.workflow_field_validator import (
    validate_workflow_field_values
)

from services.workflow_provenance_validator import (
    validate_workflow_provenance
)

from services.generic_workflow_service import (
    evaluate_generic_workflow
)


def process_workflow(
    workflow: GenericWorkflow,
    trusted_user_context: dict | None = None
):

    # ========================================================
    # STAGE 0 — INPUT SECURITY
    # ========================================================

    security_result = check_input_security(
        workflow.user_request
    )

    if not security_result["secure"]:

        return {
            "status": "blocked",
            "security": security_result,
            "workflow": workflow
        }

    # ========================================================
    # STAGE 1 — PROVENANCE VALIDATION
    #
    # IMPORTANT:
    # Validate BEFORE normalization.
    #
    # The AI cannot claim that a value was supplied by
    # the user unless that value exists in trusted context.
    # ========================================================

    provenance_result = validate_workflow_provenance(
        workflow,
        trusted_user_context
    )

    if not provenance_result["valid"]:

        return {
            "status": "invalid",
            "validation_stage": "provenance",
            "validation_errors": provenance_result["errors"],
            "security": security_result,
            "workflow": workflow
        }

    # ========================================================
    # STAGE 2 — NORMALIZATION
    # ========================================================

    normalized_workflow = normalize_workflow(
        workflow
    )

    # ========================================================
    # STAGE 3 — STRUCTURAL VALIDATION
    # ========================================================

    validation_result = validate_workflow(
        normalized_workflow
    )

    if not validation_result["valid"]:

        return {
            "status": "invalid",
            "validation_stage": "structure",
            "validation_errors": validation_result["errors"],
            "security": security_result,
            "workflow": normalized_workflow
        }

    # ========================================================
    # STAGE 4 — FIELD VALUE VALIDATION
    # ========================================================

    field_value_result = validate_workflow_field_values(
        normalized_workflow
    )

    if not field_value_result["valid"]:

        return {
            "status": "invalid",
            "validation_stage": "field_values",
            "validation_errors": field_value_result["errors"],
            "security": security_result,
            "workflow": normalized_workflow
        }

    # ========================================================
    # STAGE 5 — WORKFLOW EVALUATION
    # ========================================================

    evaluation_result = evaluate_generic_workflow(
        normalized_workflow
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {
        "status": "valid",
        "security": security_result,
        "workflow": normalized_workflow,
        "validation": validation_result,
        "field_value_validation": field_value_result,
        "provenance_validation": provenance_result,
        "evaluation": evaluation_result
    }