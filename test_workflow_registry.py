from services.workflow_registry import (
    resolve_workflow_type,
    get_workflow_definition,
)


# =========================================
# TEST 1: Canonical workflow type
# =========================================

result = resolve_workflow_type(
    "travel_planning"
)

print("\nTEST 1 — CANONICAL WORKFLOW")
print(result)

assert result == "travel_planning"


# =========================================
# TEST 2: Alias
# =========================================

result = resolve_workflow_type(
    "trip_planning"
)

print("\nTEST 2 — ALIAS")
print(result)

assert result == "travel_planning"


# =========================================
# TEST 3: Another alias
# =========================================

result = resolve_workflow_type(
    "vacation_planning"
)

print("\nTEST 3 — VACATION ALIAS")
print(result)

assert result == "travel_planning"


# =========================================
# TEST 4: Image generation alias
# =========================================

result = resolve_workflow_type(
    "image_creation"
)

print("\nTEST 4 — IMAGE ALIAS")
print(result)

assert result == "image_generation"


# =========================================
# TEST 5: Interview preparation alias
# =========================================

result = resolve_workflow_type(
    "interview_prep"
)

print("\nTEST 5 — INTERVIEW ALIAS")
print(result)

assert result == "interview_preparation"


# =========================================
# TEST 6: Unknown workflow
# =========================================

result = resolve_workflow_type(
    "drone_battery_maintenance"
)

print("\nTEST 6 — UNKNOWN WORKFLOW")
print(result)

assert result is None


# =========================================
# TEST 7: Get workflow definition
# =========================================

definition = get_workflow_definition(
    "trip_planning"
)

print("\nTEST 7 — WORKFLOW DEFINITION")
print(definition)

assert definition is not None
assert "fields" in definition
assert "aliases" in definition


# =========================================
# TEST 8: Verify canonical fields
# =========================================

fields = definition["fields"]

print("\nTEST 8 — CANONICAL FIELDS")
print(fields)

assert "destination" in fields
assert "start_date" in fields
assert "number_of_people" in fields
assert "trip_duration_days" in fields


# =========================================
# TEST 9: Verify field types
# =========================================

assert fields["destination"]["field_type"] == "string"

assert fields["start_date"]["field_type"] == "date"

assert fields["number_of_people"]["field_type"] == "integer"

assert fields["trip_duration_days"]["field_type"] == "integer"


# =========================================
# TEST 10: Case normalization
# =========================================

result = resolve_workflow_type(
    "TRIP_PLANNING"
)

print("\nTEST 10 — CASE NORMALIZATION")
print(result)

assert result == "travel_planning"


print("\nALL WORKFLOW REGISTRY TESTS PASSED")