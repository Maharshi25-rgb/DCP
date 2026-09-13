from models.generic_workflow import GenericWorkflow


def confirm_suggestion(
    workflow: GenericWorkflow,
    suggestion_value: str
):
    """
    Confirm one AI suggestion.

    Only a pending suggestion can be confirmed.
    """

    for suggestion in workflow.suggestions:

        if (
            suggestion.value.lower() == suggestion_value.lower()
            and suggestion.status == "pending_confirmation"
        ):
            suggestion.status = "user_confirmed"

            return {
                "success": True,
                "message": f"'{suggestion.value}' confirmed by user."
            }

    return {
        "success": False,
        "message": f"Suggestion '{suggestion_value}' not found."
    }


def reject_suggestion(
    workflow: GenericWorkflow,
    suggestion_value: str
):
    """
    Reject one AI suggestion.
    """

    for suggestion in workflow.suggestions:

        if (
            suggestion.value.lower() == suggestion_value.lower()
            and suggestion.status == "pending_confirmation"
        ):
            suggestion.status = "rejected"

            return {
                "success": True,
                "message": f"'{suggestion.value}' rejected by user."
            }

    return {
        "success": False,
        "message": f"Suggestion '{suggestion_value}' not found."
    }


def confirm_all_suggestions(
    workflow: GenericWorkflow
):
    """
    Confirm every pending AI suggestion.
    """

    confirmed = []

    for suggestion in workflow.suggestions:

        if suggestion.status == "pending_confirmation":

            suggestion.status = "user_confirmed"

            confirmed.append(suggestion.value)

    return {
        "success": True,
        "confirmed": confirmed
    }


def reject_all_suggestions(
    workflow: GenericWorkflow
):
    """
    Reject every pending AI suggestion.
    """

    rejected = []

    for suggestion in workflow.suggestions:

        if suggestion.status == "pending_confirmation":

            suggestion.status = "rejected"

            rejected.append(suggestion.value)

    return {
        "success": True,
        "rejected": rejected
    }

def confirm_selected_suggestions(
    workflow: GenericWorkflow,
    selected_values: list[str],
):
    """
    Confirm only the suggestions explicitly selected by the user.
    """

    confirmed = []
    not_found = []

    selected_values_normalized = {
        value.strip().lower()
        for value in selected_values
    }

    for suggestion in workflow.suggestions:

        if (
            suggestion.value.strip().lower()
            in selected_values_normalized
            and suggestion.status == "pending_confirmation"
        ):
            suggestion.status = "user_confirmed"
            confirmed.append(suggestion.value)

    for value in selected_values:

        found = any(
            suggestion.value.strip().lower() == value.strip().lower()
            and suggestion.status == "user_confirmed"
            for suggestion in workflow.suggestions
        )

        if not found:
            not_found.append(value)

    return {
        "success": True,
        "confirmed": confirmed,
        "not_found": not_found,
    }