from models.generic_workflow import WorkflowField, GenericWorkflow


def generate_workflow(user_request: str):

    request = user_request.lower()

    if "travel" in request or "trip" in request or "visit" in request:

        fields = [
            WorkflowField(
                field_name="destination",
                value=None,
                required=True,
                question="Where do you want to travel?"
            ),
            WorkflowField(
                field_name="number_of_people",
                value=None,
                required=True,
                question="How many people are travelling?"
            ),
            WorkflowField(
                field_name="number_of_days",
                value=None,
                required=True,
                question="How many days do you want to travel?"
            ),
            WorkflowField(
                field_name="budget",
                value=None,
                required=True,
                question="What is your budget?"
            ),
            WorkflowField(
                field_name="hotel_preference",
                value=None,
                required=False,
                question="What type of hotel do you prefer?"
            )
        ]

        workflow_type = "travel"

    else:

        fields = []

        workflow_type = "unknown"

    workflow = GenericWorkflow(
        workflow_type=workflow_type,
        user_request=user_request,
        fields=fields,
        next_action="collect_information"
    )

    return workflow