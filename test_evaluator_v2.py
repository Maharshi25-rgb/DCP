from models.generic_workflow import (
    GenericWorkflow,
    WorkflowField,
    WorkflowSuggestion
)

from services.generic_workflow_service import evaluate_generic_workflow
from services.workflow_context import get_confirmed_context


workflow = GenericWorkflow(
    workflow_type="travel_planning",
    user_request="I want to visit Kerala",
    fields=[
        WorkflowField(
            field_name="destination",
            value="Kerala",
            required=True,
            question="Where do you want to travel?"
        ),
        WorkflowField(
            field_name="travel_dates",
            value="December 20 to December 25",
            required=True,
            question="What are your travel dates?"
        ),
    ],
    suggestions=[
        WorkflowSuggestion(
            field_name="places",
            value="Munnar",
            reason="Mountain and nature experiences",
            status="user_confirmed"
        ),
        WorkflowSuggestion(
            field_name="places",
            value="Kochi",
            reason="Culture and city experiences",
            status="pending_confirmation"
        ),
        WorkflowSuggestion(
            field_name="places",
            value="Thekkady",
            reason="Wildlife and nature experiences",
            status="rejected"
        ),
    ],
    next_action="generate_prompt"
)


# -----------------------------------------
# Evaluator V2
# -----------------------------------------

evaluation = evaluate_generic_workflow(workflow)

print("\n========== EVALUATOR V2 ==========\n")
print(evaluation)


# -----------------------------------------
# Confirmed Context
# -----------------------------------------

context = get_confirmed_context(workflow)

print("\n========== CONFIRMED CONTEXT ==========\n")
print(context)