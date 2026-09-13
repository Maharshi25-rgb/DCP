from services.ai_workflow_service import generate_ai_workflow


# =========================================
# INCOMPLETE USER REQUEST
# =========================================

user_request = """
Plan a trip to Kerala for 4 people.
"""


workflow = generate_ai_workflow(user_request)


print("\nGENERATED WORKFLOW")
print(workflow.model_dump_json(indent=2))


print("\nFIELDS")

for field in workflow.fields:

    print(
        f"{field.field_name}"
        f" -> value={field.value}"
        f" -> type={field.field_type}"
        f" -> required={field.required}"
        f" -> source={field.source}"
    )


print("\nSUGGESTIONS")

for suggestion in workflow.suggestions:

    print(
        f"{suggestion.field_name}"
        f" -> {suggestion.value}"
        f" -> {suggestion.status}"
    )


print("\nNEXT ACTION")
print(workflow.next_action)


# =========================================
# ASSERTIONS
# =========================================

# Workflow should be travel planning
assert workflow.workflow_type == "trip_planning"


# Destination should be extracted
destination = next(
    field
    for field in workflow.fields
    if field.field_name == "destination"
)

assert destination.value == "Kerala"
assert destination.source == "user_confirmed"


# Number of people should be extracted
people = next(
    field
    for field in workflow.fields
    if field.field_name == "number_of_people"
)

assert people.value == "4"
assert people.field_type == "integer"
assert people.source == "user_confirmed"


# There should be at least one missing required field
missing_required_fields = [
    field
    for field in workflow.fields
    if field.required and field.value is None
]

assert len(missing_required_fields) > 0


# The AI must NOT invent values for missing fields
for field in missing_required_fields:

    assert field.value is None


# Workflow should request more information
assert workflow.next_action == "collect_information"


print("\nINCOMPLETE AI WORKFLOW TEST PASSED")