from models.generic_workflow import (
    GenericWorkflow,
    WorkflowField
)

from services.output_repair_service import (
    repair_ai_output
)

from services.output_validator import (
    validate_ai_output
)


# ============================================================
# TEST WORKFLOW
# ============================================================

workflow = GenericWorkflow(
    workflow_type="travel_planning",
    user_request="Plan a trip to Kerala for 4 people for 5 days",
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


# ============================================================
# TEST 1 — INVALID RESPONSE CAN BE REPAIRED
# ============================================================

bad_response = """
Here is a 10-day trip to Goa for 8 people.
"""

validation = validate_ai_output(
    bad_response,
    workflow
)

assert validation["valid"] is False

result = repair_ai_output(
    bad_response,
    workflow,
    validation
)

assert result["success"] is True

assert isinstance(
    result["response"],
    str
)

assert len(
    result["response"]
) > 0

print(
    "TEST 1 PASSED — invalid response repaired"
)


# ============================================================
# TEST 2 — REPAIRED RESPONSE SHOULD RESPECT WORKFLOW
# ============================================================

repaired_response = result["response"]

revalidation = validate_ai_output(
    repaired_response,
    workflow
)

assert revalidation["valid"] is True

print(
    "TEST 2 PASSED — repaired response passes validation"
)


# ============================================================
# TEST 3 — DESTINATION MUST REMAIN KERALA
# ============================================================

assert "kerala" in repaired_response.lower()

assert "goa" not in repaired_response.lower()

print(
    "TEST 3 PASSED — destination preserved"
)


# ============================================================
# TEST 4 — PEOPLE COUNT MUST REMAIN 4
# ============================================================

revalidation = validate_ai_output(
    repaired_response,
    workflow
)

assert not any(
    contradiction["field_name"]
    == "number_of_people"
    for contradiction
    in revalidation["contradictions"]
)

print(
    "TEST 4 PASSED — people count preserved"
)


# ============================================================
# TEST 5 — DURATION MUST REMAIN 5 DAYS
# ============================================================

assert not any(
    contradiction["field_name"]
    == "trip_duration_days"
    for contradiction
    in revalidation["contradictions"]
)

print(
    "TEST 5 PASSED — duration preserved"
)


# ============================================================
# TEST 6 — EMPTY ORIGINAL RESPONSE
# ============================================================

result = repair_ai_output(
    "",
    workflow,
    {
        "valid": False,
        "errors": [
            "AI response cannot be empty."
        ]
    }
)

assert result["success"] is False

assert result["response"] is None

print(
    "TEST 6 PASSED — empty response rejected"
)


# ============================================================
# TEST 7 — NON-STRING ORIGINAL RESPONSE
# ============================================================

result = repair_ai_output(
    None,
    workflow,
    {
        "valid": False,
        "errors": [
            "Invalid response type."
        ]
    }
)

assert result["success"] is False

print(
    "TEST 7 PASSED — non-string response rejected"
)


# ============================================================
# TEST 8 — INVALID VALIDATION RESULT
# ============================================================

result = repair_ai_output(
    "Some response",
    workflow,
    None
)

assert result["success"] is False

print(
    "TEST 8 PASSED — invalid validation result rejected"
)


# ============================================================
# TEST 9 — REPAIR OUTPUT IS USER-FACING
# ============================================================

assert "dcp" not in repaired_response.lower()

assert "validation" not in repaired_response.lower()

print(
    "TEST 9 PASSED — internal DCP details excluded"
)


# ============================================================
# TEST 10 — SECOND VALIDATION
# ============================================================

final_validation = validate_ai_output(
    repaired_response,
    workflow
)

assert final_validation["valid"] is True

print(
    "TEST 10 PASSED — final repaired response validated"
)


# ============================================================
# FINAL
# ============================================================

print()
print(
    "ALL OUTPUT REPAIR SERVICE TESTS PASSED"
)