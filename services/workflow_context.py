from models.generic_workflow import GenericWorkflow


def get_confirmed_context(workflow: GenericWorkflow):
    """
    Return only information that DCP is allowed to treat
    as confirmed user information.
    """

    confirmed_information = []

    # Information directly provided by the user
    for field in workflow.fields:

        if (
            field.value is not None
            and field.source == "user_confirmed"
        ):
            confirmed_information.append({
                "field_name": field.field_name,
                "value": field.value,
                "source": "user_confirmed",
            })

    # Information explicitly confirmed from AI suggestions
    for suggestion in workflow.suggestions:

        if suggestion.status == "user_confirmed":
            confirmed_information.append({
                "field_name": suggestion.field_name,
                "value": suggestion.value,
                "source": "user_confirmed",
            })

    return confirmed_information