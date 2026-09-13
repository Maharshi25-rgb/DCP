from models.generic_workflow import (
    GenericWorkflow,
    WorkflowField
)

from services.workflow_field_validator import (
    validate_workflow_field_values
)


# -----------------------------------------
# Test 1: Valid fields
# -----------------------------------------

workflow = GenericWorkflow(

    workflow_type="travel_planning",

    user_request="Plan my trip",

    fields=[
        WorkflowField(
            field_name="destination",
            value="Kerala",
            field_type="string",
            required=True,
            question="Where do you want to travel?"
        ),

        WorkflowField(
            field_name="number_of_people",
            value="4",
            field_type="integer",
            required=True,
            question="How many people are travelling?"
        ),

        WorkflowField(
            field_name="start_date",
            value="2026-12-20",
            field_type="date",
            required=True,
            question="What is the start date?"
        )
    ],

    next_action="generate_prompt"
)


result = validate_workflow_field_values(workflow)

print("\nTEST 1")
print(result)

assert result["valid"] is True
assert result["errors"] == []


# -----------------------------------------
# Test 2: Invalid integer
# -----------------------------------------

workflow.fields[1].value = "four"

result = validate_workflow_field_values(workflow)

print("\nTEST 2")
print(result)

assert result["valid"] is False
assert len(result["errors"]) == 1

assert (
    result["errors"][0]["field_name"]
    == "number_of_people"
)


# -----------------------------------------
# Test 3: Invalid date
# -----------------------------------------

workflow.fields[1].value = "4"
workflow.fields[2].value = "20-12-2026"

result = validate_workflow_field_values(workflow)

print("\nTEST 3")
print(result)

assert result["valid"] is False

assert (
    result["errors"][0]["field_name"]
    == "start_date"
)


# -----------------------------------------
# Test 4: Missing value
# -----------------------------------------

workflow.fields[2].value = None

result = validate_workflow_field_values(workflow)

print("\nTEST 4")
print(result)

assert result["valid"] is True

print("\nALL WORKFLOW FIELD VALIDATOR TESTS PASSED")