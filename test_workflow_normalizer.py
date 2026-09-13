from models.generic_workflow import (
    GenericWorkflow,
    WorkflowField
)

from services.workflow_normalizer import normalize_workflow


# =========================================
# TEST 1: Canonical workflow remains same
# =========================================

workflow = GenericWorkflow(

    workflow_type="travel_planning",

    user_request="Plan my trip to Kerala",

    fields=[
        WorkflowField(
            field_name="destination",
            value="Kerala",
            field_type="string",
            required=True,
            question="Where do you want to travel?",
            source="user_confirmed"
        ),

        WorkflowField(
            field_name="number_of_people",
            value="4",
            field_type="string",
            required=False,
            question="How many people are travelling?",
            source="user_confirmed"
        )
    ],

    next_action="generate_prompt"
)


result = normalize_workflow(workflow)

print("\nTEST 1 — CANONICAL WORKFLOW")
print(result.model_dump())

assert result.workflow_type == "travel_planning"


# =========================================
# TEST 2: Alias normalization
# =========================================

workflow = GenericWorkflow(

    workflow_type="trip_planning",

    user_request="Plan my trip to Kerala",

    fields=[
        WorkflowField(
            field_name="destination",
            value="Kerala",
            field_type="string",
            required=True,
            question="Where do you want to travel?",
            source="user_confirmed"
        )
    ],

    next_action="generate_prompt"
)


result = normalize_workflow(workflow)

print("\nTEST 2 — ALIAS NORMALIZATION")
print(result.model_dump())

assert result.workflow_type == "travel_planning"


# =========================================
# TEST 3: Canonical field type correction
# =========================================

workflow = GenericWorkflow(

    workflow_type="trip_planning",

    user_request="Plan my trip",

    fields=[
        WorkflowField(
            field_name="number_of_people",
            value="4",
            field_type="string",
            required=False,
            question="How many people?",
            source="user_confirmed"
        )
    ],

    next_action="generate_prompt"
)


result = normalize_workflow(workflow)

print("\nTEST 3 — FIELD TYPE NORMALIZATION")
print(result.model_dump())

field = next(
    field
    for field in result.fields
    if field.field_name == "number_of_people"
)

assert field.field_type == "integer"
assert field.required is True


# =========================================
# TEST 4: User value must be preserved
# =========================================

assert field.value == "4"
assert field.source == "user_confirmed"

print("\nTEST 4 — USER VALUE PRESERVED")
print(
    f"value={field.value}, "
    f"source={field.source}"
)


# =========================================
# TEST 5: Missing canonical fields added
# =========================================

workflow = GenericWorkflow(

    workflow_type="trip_planning",

    user_request="Plan my trip to Kerala",

    fields=[
        WorkflowField(
            field_name="destination",
            value="Kerala",
            field_type="string",
            required=True,
            question="Where do you want to travel?",
            source="user_confirmed"
        )
    ],

    next_action="generate_prompt"
)


result = normalize_workflow(workflow)

print("\nTEST 5 — MISSING CANONICAL FIELDS")
print(result.model_dump())


field_names = {
    field.field_name
    for field in result.fields
}


assert "destination" in field_names
assert "start_date" in field_names
assert "number_of_people" in field_names
assert "trip_duration_days" in field_names


# =========================================
# TEST 6: Added fields are missing
# =========================================

start_date = next(
    field
    for field in result.fields
    if field.field_name == "start_date"
)

duration = next(
    field
    for field in result.fields
    if field.field_name == "trip_duration_days"
)


assert start_date.value is None
assert start_date.source == "missing"
assert start_date.field_type == "date"
assert start_date.required is True


assert duration.value is None
assert duration.source == "missing"
assert duration.field_type == "integer"
assert duration.required is True


# =========================================
# TEST 7: Unknown workflow remains dynamic
# =========================================

workflow = GenericWorkflow(

    workflow_type="drone_battery_maintenance",

    user_request="Create a drone battery maintenance workflow",

    fields=[
        WorkflowField(
            field_name="battery_type",
            value="LiPo",
            field_type="string",
            required=True,
            question="What type of battery is used?",
            source="user_confirmed"
        )
    ],

    next_action="generate_prompt"
)


result = normalize_workflow(workflow)

print("\nTEST 7 — UNKNOWN WORKFLOW")
print(result.model_dump())

assert result.workflow_type == "drone_battery_maintenance"
assert result.fields[0].value == "LiPo"


# =========================================
# TEST 8: Unknown field in known workflow
# =========================================

workflow = GenericWorkflow(

    workflow_type="trip_planning",

    user_request="Plan my trip",

    fields=[
        WorkflowField(
            field_name="custom_requirement",
            value="Beach hotel",
            field_type="string",
            required=True,
            question="Any custom requirement?",
            source="user_confirmed"
        )
    ],

    next_action="generate_prompt"
)


result = normalize_workflow(workflow)

print("\nTEST 8 — UNKNOWN FIELD PRESERVED")
print(result.model_dump())

assert result.workflow_type == "travel_planning"
assert result.fields[0].field_name == "custom_requirement"
assert result.fields[0].value == "Beach hotel"


# =========================================
# TEST 9: Existing canonical fields not duplicated
# =========================================

field_name_list = [
    field.field_name
    for field in result.fields
]

assert field_name_list.count("custom_requirement") == 1


print("\nALL WORKFLOW NORMALIZER TESTS PASSED")