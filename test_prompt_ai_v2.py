from models.generic_workflow import (
    GenericWorkflow,
    WorkflowField,
    WorkflowSuggestion
)

from services.prompt_service import build_prompt
from services.ai_response_service import generate_ai_response


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
# Build Prompt
# -----------------------------------------

prompt = build_prompt(workflow)

print("\n========== GENERATED PROMPT ==========\n")
print(prompt)


# -----------------------------------------
# Generate AI Response
# -----------------------------------------

print("\n========== AI RESPONSE ==========\n")

response = generate_ai_response(prompt)

print(response)