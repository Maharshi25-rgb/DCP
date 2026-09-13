from models.generic_workflow import (
    GenericWorkflow,
    WorkflowSuggestion,
)


def generate_filtered_suggestions(
    workflow: GenericWorkflow,
    candidates: list[WorkflowSuggestion],
):
    """
    Filter candidate suggestions against information
    already known by the workflow.
    """

    filtered_suggestions = []

    # Collect values already mentioned by the user
    user_values = set()

    for field in workflow.fields:

        if field.value is not None:
            user_values.add(field.value.strip().lower())

    # Collect suggestion values that should not be suggested again
    blocked_values = set(user_values)

    for suggestion in workflow.suggestions:

        if suggestion.status in {
            "user_confirmed",
            "rejected",
        }:
            blocked_values.add(
                suggestion.value.strip().lower()
            )

    # Filter candidates
    for candidate in candidates:

        candidate_value = candidate.value.strip().lower()

        # Skip information already known or previously handled
        if candidate_value in blocked_values:
            continue

        filtered_suggestions.append(candidate)

        # Prevent duplicate candidates in the same batch
        blocked_values.add(candidate_value)

    return filtered_suggestions


def add_suggestions_to_workflow(
    workflow: GenericWorkflow,
    candidates: list[WorkflowSuggestion],
):
    """
    Generate filtered suggestions and attach only
    new suggestions to the workflow.
    """

    filtered_suggestions = generate_filtered_suggestions(
        workflow,
        candidates,
    )

    existing_values = {
        suggestion.value.strip().lower()
        for suggestion in workflow.suggestions
    }

    new_suggestions = []

    for suggestion in filtered_suggestions:

        suggestion_value = suggestion.value.strip().lower()

        if suggestion_value not in existing_values:

            new_suggestions.append(suggestion)

            existing_values.add(suggestion_value)

    workflow.suggestions.extend(new_suggestions)

    return workflow