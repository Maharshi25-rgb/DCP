from services.ai_workflow_service import generate_ai_workflow


user_request = """
Plan a 5 day trip to Kerala for 4 people.
The trip starts on 2026-12-20.
Our budget is 50000 rupees.
"""


workflow = generate_ai_workflow(user_request)


print("\nGENERATED WORKFLOW")
print(workflow.model_dump_json(indent=2))


print("\nFIELD TYPES")

for field in workflow.fields:

    print(
        f"{field.field_name}"
        f" -> {field.field_type}"
        f" -> {field.value}"
    )


print("\nNEXT ACTION")
print(workflow.next_action)


# -----------------------------------------
# Basic assertions
# -----------------------------------------

assert workflow.workflow_type == "travel_planning"

assert workflow.next_action in {
    "collect_information",
    "generate_prompt",
    "complete"
}


field_types = {
    field.field_name: field.field_type
    for field in workflow.fields
}


# These fields should normally be typed
# correctly by the AI.

if "number_of_people" in field_types:

    assert field_types["number_of_people"] == "integer"

if "start_date" in field_types:

    assert field_types["start_date"] == "date"

if "budget" in field_types:

    assert field_types["budget"] == "integer"


print("\nAI WORKFLOW FIELD TYPE TEST PASSED")