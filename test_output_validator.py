from models.generic_workflow import (
    GenericWorkflow,
    WorkflowField
)

from services.output_validator import (
    validate_ai_output
)


# ============================================================
# TEST 1 — VALID RESPONSE
# ============================================================

workflow = GenericWorkflow(
    workflow_type="travel_planning",
    user_request="Plan a trip to Kerala",
    fields=[
        WorkflowField(
            field_name="destination",
            value="Kerala",
            field_type="string",
            required=True,
            question="Where?",
            source="user_confirmed"
        ),
        WorkflowField(
            field_name="number_of_people",
            value="4",
            field_type="integer",
            required=True,
            question="How many people?",
            source="user_confirmed"
        ),
        WorkflowField(
            field_name="trip_duration_days",
            value="5",
            field_type="integer",
            required=True,
            question="How many days?",
            source="user_confirmed"
        )
    ],
    next_action="generate_prompt"
)

response = """
Here is a 5-day trip to Kerala for 4 people.
"""

result = validate_ai_output(
    response,
    workflow
)

assert result["valid"] is True
assert result["contradictions"] == []

print("TEST 1 PASSED — valid response")


# ============================================================
# TEST 2 — EMPTY RESPONSE
# ============================================================

result = validate_ai_output(
    "",
    workflow
)

assert result["valid"] is False

print("TEST 2 PASSED — empty response rejected")


# ============================================================
# TEST 3 — NON-STRING RESPONSE
# ============================================================

result = validate_ai_output(
    None,
    workflow
)

assert result["valid"] is False

print("TEST 3 PASSED — non-string response rejected")


# ============================================================
# TEST 4 — DESTINATION CONTRADICTION
# ============================================================

response = """
Here is a 5-day trip to Goa for 4 people.
"""

result = validate_ai_output(
    response,
    workflow
)

assert result["valid"] is False

assert any(
    contradiction["field_name"]
    == "destination"
    for contradiction in result["contradictions"]
)

print(
    "TEST 4 PASSED — destination contradiction detected"
)


# ============================================================
# TEST 5 — PEOPLE COUNT CONTRADICTION
# ============================================================

response = """
Here is a 5-day trip to Kerala for 6 people.
"""

result = validate_ai_output(
    response,
    workflow
)

assert result["valid"] is False

assert any(
    contradiction["field_name"]
    == "number_of_people"
    for contradiction in result["contradictions"]
)

print(
    "TEST 5 PASSED — people count contradiction detected"
)


# ============================================================
# TEST 6 — DURATION CONTRADICTION
# ============================================================

response = """
Here is a 10-day trip to Kerala for 4 people.
"""

result = validate_ai_output(
    response,
    workflow
)

assert result["valid"] is False

assert any(
    contradiction["field_name"]
    == "trip_duration_days"
    for contradiction in result["contradictions"]
)

print(
    "TEST 6 PASSED — duration contradiction detected"
)


# ============================================================
# TEST 7 — MISSING CONFIRMED VALUE
# ============================================================

response = """
Kerala is a beautiful destination.
"""

result = validate_ai_output(
    response,
    workflow
)

assert result["valid"] is True

assert "destination" in result["checked_fields"]

assert len(
    result["warnings"]
) > 0

print(
    "TEST 7 PASSED — missing explicit value produces warning"
)


# ============================================================
# TEST 8 — OPTIONAL AI-GENERATED INFORMATION
# ============================================================

workflow = GenericWorkflow(
    workflow_type="travel_planning",
    user_request="Plan a trip to Kerala",
    fields=[
        WorkflowField(
            field_name="destination",
            value="Kerala",
            field_type="string",
            required=True,
            question="Where?",
            source="user_confirmed"
        ),
        WorkflowField(
            field_name="budget",
            value="50000",
            field_type="integer",
            required=False,
            question="What is your budget?",
            source="ai_suggested"
        )
    ],
    next_action="generate_prompt"
)

response = """
Kerala is a good destination for your trip.
"""

result = validate_ai_output(
    response,
    workflow
)

assert result["valid"] is True

assert (
    "budget"
    not in result["checked_fields"]
)

print(
    "TEST 8 PASSED — non-user-confirmed field not treated as trusted"
)


# ============================================================
# TEST 9 — MULTIPLE CONTRADICTIONS
# ============================================================

workflow = GenericWorkflow(
    workflow_type="travel_planning",
    user_request="Plan a trip to Kerala",
    fields=[
        WorkflowField(
            field_name="destination",
            value="Kerala",
            field_type="string",
            required=True,
            question="Where?",
            source="user_confirmed"
        ),
        WorkflowField(
            field_name="number_of_people",
            value="4",
            field_type="integer",
            required=True,
            question="How many people?",
            source="user_confirmed"
        ),
        WorkflowField(
            field_name="trip_duration_days",
            value="5",
            field_type="integer",
            required=True,
            question="How many days?",
            source="user_confirmed"
        )
    ],
    next_action="generate_prompt"
)

response = """
Here is a 10-day trip to Goa for 8 people.
"""

result = validate_ai_output(
    response,
    workflow
)

assert result["valid"] is False

assert len(
    result["contradictions"]
) >= 2

print(
    "TEST 9 PASSED — multiple contradictions detected"
)


# ============================================================
# TEST 10 — NORMAL RESPONSE WITH ADDITIONAL INFORMATION
# ============================================================

workflow = GenericWorkflow(
    workflow_type="travel_planning",
    user_request="Plan a trip to Kerala",
    fields=[
        WorkflowField(
            field_name="destination",
            value="Kerala",
            field_type="string",
            required=True,
            question="Where?",
            source="user_confirmed"
        ),
        WorkflowField(
            field_name="number_of_people",
            value="4",
            field_type="integer",
            required=True,
            question="How many people?",
            source="user_confirmed"
        )
    ],
    next_action="generate_prompt"
)

response = """
Here is your Kerala travel plan for 4 people.

Day 1: Kochi
Day 2: Munnar
Day 3: Thekkady
Day 4: Alleppey
"""

result = validate_ai_output(
    response,
    workflow
)

assert result["valid"] is True

assert len(
    result["checked_fields"]
) == 2

print(
    "TEST 10 PASSED — valid response with additional information"
)


# ============================================================
# FINAL
# ============================================================

print()
print("ALL OUTPUT VALIDATOR TESTS PASSED")