import re

from models.generic_workflow import GenericWorkflow


ALLOWED_NEXT_ACTIONS = {
    "collect_information",
    "generate_prompt",
    "complete",
}


def is_snake_case(value: str) -> bool:
    return bool(
        re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", value)
    )


def validate_workflow(workflow: GenericWorkflow):

    errors = []

    # -----------------------------------------
    # 1. Validate workflow_type
    # -----------------------------------------

    if not is_snake_case(workflow.workflow_type):

        errors.append(
            f"Invalid workflow_type: '{workflow.workflow_type}'. "
            "Must use lowercase snake_case."
        )

    # -----------------------------------------
    # 2. Validate next_action
    # -----------------------------------------

    if workflow.next_action not in ALLOWED_NEXT_ACTIONS:

        errors.append(
            f"Invalid next_action: '{workflow.next_action}'. "
            f"Allowed values: {sorted(ALLOWED_NEXT_ACTIONS)}"
        )

    # -----------------------------------------
    # 3. Validate fields
    # -----------------------------------------

    field_names = set()

    for field in workflow.fields:

        # Field name
        if not is_snake_case(field.field_name):

            errors.append(
                f"Invalid field_name: '{field.field_name}'. "
                "Must use lowercase snake_case."
            )

        # Duplicate field
        if field.field_name in field_names:

            errors.append(
                f"Duplicate field_name: '{field.field_name}'."
            )

        field_names.add(field.field_name)

        # Required field question
        if field.required and field.value is None:

            if not field.question.strip():

                errors.append(
                    f"Required field '{field.field_name}' "
                    "is missing a question."
                )

        # -----------------------------------------
        # 3A. Missing value must have source=missing
        # -----------------------------------------

        if field.value is None:

            if field.source != "missing":

                errors.append(
                    f"Field '{field.field_name}' has no value "
                    f"but source is '{field.source}'. "
                    "Missing fields must use source='missing'."
                )

        # -----------------------------------------
        # 3B. Value cannot use source=missing
        # -----------------------------------------

        if field.value is not None:

            if field.source == "missing":

                errors.append(
                    f"Field '{field.field_name}' has a value "
                    "but source='missing'."
                )

    # -----------------------------------------
    # 4. Validate suggestions
    # -----------------------------------------

    field_values = {
        field.value.strip().lower()
        for field in workflow.fields
        if field.value is not None
    }

    for suggestion in workflow.suggestions:

        suggestion_value = suggestion.value.strip().lower()

        # -----------------------------------------
        # 4A. Empty / placeholder suggestions
        # -----------------------------------------

        invalid_suggestion_values = {
            "",
            "null",
            "none",
            "n/a",
            "unknown",
        }

        if suggestion_value in invalid_suggestion_values:

            errors.append(
                f"Invalid suggestion value for "
                f"'{suggestion.field_name}': "
                f"'{suggestion.value}'. "
                "Suggestions must contain a concrete value."
            )

        # -----------------------------------------
        # 4B. Suggestion duplicates known information
        # -----------------------------------------

        if suggestion_value in field_values:

            errors.append(
                f"Suggestion '{suggestion.value}' for "
                f"'{suggestion.field_name}' duplicates "
                "information already present in the workflow."
            )

    # -----------------------------------------
    # 5. Return result
    # -----------------------------------------

    if errors:

        return {
            "valid": False,
            "errors": errors
        }

    return {
        "valid": True,
        "errors": []
    }