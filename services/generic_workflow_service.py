from models.generic_workflow import GenericWorkflow


def evaluate_generic_workflow(workflow: GenericWorkflow):

    filled_fields = []
    missing_required_fields = []
    optional_missing_fields = []

    # -----------------------------------------
    # 1. Evaluate workflow fields
    # -----------------------------------------

    for field in workflow.fields:

        if field.value is not None:

            filled_fields.append({
                "field_name": field.field_name,
                "value": field.value,
                "source": field.source
            })

        elif field.required:

            missing_required_fields.append({
                "field_name": field.field_name,
                "question": field.question
            })

        else:

            optional_missing_fields.append({
                "field_name": field.field_name,
                "question": field.question
            })

    # -----------------------------------------
    # 2. Evaluate suggestions
    # -----------------------------------------

    confirmed_suggestions = []
    pending_suggestions = []
    rejected_suggestions = []

    for suggestion in workflow.suggestions:

        suggestion_data = {
            "field_name": suggestion.field_name,
            "value": suggestion.value,
            "reason": suggestion.reason,
            "status": suggestion.status
        }

        if suggestion.status == "user_confirmed":

            confirmed_suggestions.append(suggestion_data)

        elif suggestion.status == "pending_confirmation":

            pending_suggestions.append(suggestion_data)

        elif suggestion.status == "rejected":

            rejected_suggestions.append(suggestion_data)

    # -----------------------------------------
    # 3. Determine workflow status
    # -----------------------------------------

    if missing_required_fields:

        status = "incomplete"
        next_action = "request_user_decision"

    else:

        status = "complete"
        next_action = "generate_prompt"

    # -----------------------------------------
    # 4. Return evaluation result
    # -----------------------------------------

    return {
        "status": status,
        "next_action": next_action,

        "filled_fields": filled_fields,

        "missing_required_fields": missing_required_fields,

        "optional_missing_fields": optional_missing_fields,

        "confirmed_suggestions": confirmed_suggestions,

        "pending_suggestions": pending_suggestions,

        "rejected_suggestions": rejected_suggestions
    }


def update_workflow_with_answers(
    workflow: GenericWorkflow,
    user_answers: dict
):

    for field in workflow.fields:

        if field.field_name in user_answers:

            field.value = user_answers[field.field_name]
            field.source = "user_confirmed"

    return workflow