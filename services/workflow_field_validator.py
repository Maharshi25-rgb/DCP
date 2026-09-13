from models.generic_workflow import GenericWorkflow

from services.field_value_validator import validate_field_value


def validate_workflow_field_values(
    workflow: GenericWorkflow
):
    """
    Validate every field value in a GenericWorkflow
    against its declared field_type.
    """

    errors = []

    for field in workflow.fields:

        result = validate_field_value(
            value=field.value,
            field_type=field.field_type
        )

        if not result["valid"]:

            errors.append({
                "field_name": field.field_name,
                "field_type": field.field_type,
                "value": field.value,
                "error": result["error"]
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