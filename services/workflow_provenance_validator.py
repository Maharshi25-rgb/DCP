from models.generic_workflow import GenericWorkflow


ALLOWED_SOURCES = {
    "user_confirmed",
    "ai_suggested",
    "assumed",
    "missing",
}


def validate_workflow_provenance(
    workflow: GenericWorkflow,
    trusted_user_context: dict | None = None
):
    """
    Validate workflow provenance.

    Values are compared using normalized string representation
    so that 5 and "5" represent the same confirmed value.
    """

    errors = []

    if trusted_user_context is None:
        trusted_user_context = {
            "confirmed_fields": {}
        }

    confirmed_fields = trusted_user_context.get(
        "confirmed_fields",
        {}
    )

    if not isinstance(confirmed_fields, dict):
        confirmed_fields = {}

    for field in workflow.fields:

        if field.source not in ALLOWED_SOURCES:
            errors.append({
                "field_name": field.field_name,
                "source": field.source,
                "error": "Invalid provenance source."
            })
            continue

        if field.value is None:

            if field.source != "missing":
                errors.append({
                    "field_name": field.field_name,
                    "source": field.source,
                    "error": (
                        "A field without a value must use "
                        "source='missing'."
                    )
                })

            continue

        if field.source == "missing":
            errors.append({
                "field_name": field.field_name,
                "source": field.source,
                "error": (
                    "A field with a value cannot use "
                    "source='missing'."
                )
            })

        if field.source == "user_confirmed":

            if field.field_name not in confirmed_fields:

                errors.append({
                    "field_name": field.field_name,
                    "value": field.value,
                    "source": field.source,
                    "error": (
                        "Field is marked user_confirmed but "
                        "was not supplied by the user."
                    )
                })

            elif str(
                confirmed_fields[field.field_name]
            ) != str(field.value):

                errors.append({
                    "field_name": field.field_name,
                    "value": field.value,
                    "source": field.source,
                    "trusted_value": confirmed_fields[
                        field.field_name
                    ],
                    "error": (
                        "Workflow value does not match the "
                        "user-confirmed value."
                    )
                })

    for suggestion in workflow.suggestions:

        if suggestion.status not in {
            "pending_confirmation",
            "user_confirmed",
            "rejected",
        }:

            errors.append({
                "field_name": suggestion.field_name,
                "status": suggestion.status,
                "error": "Invalid suggestion status."
            })

    if errors:
        return {
            "valid": False,
            "errors": errors
        }

    return {
        "valid": True,
        "errors": []
    }
