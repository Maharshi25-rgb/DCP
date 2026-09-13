from models.generic_workflow import (
    GenericWorkflow,
    WorkflowField
)

from services.ai_output_checker import (
    check_ai_output
)


# ============================================================
# TEST 1 — EMPTY RESPONSE
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
        )
    ],
    next_action="generate_prompt"
)

result = check_ai_output(
    "",
    workflow
)

assert result["valid"] is False
assert result["confidence"] == 0.0

print(
    "TEST 1 PASSED — empty response rejected"
)


# ============================================================
# TEST 2 — NON-STRING RESPONSE
# ============================================================

result = check_ai_output(
    None,
    workflow
)

assert result["valid"] is False
assert result["confidence"] == 0.0

print(
    "TEST 2 PASSED — non-string response rejected"
)


# ============================================================
# TEST 3 — VALID RESPONSE
# ============================================================

response = """
Here is a 5-day trip to Kerala for 4 people.
"""

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

result = check_ai_output(
    response,
    workflow
)

assert result["valid"] is True
assert result["confidence"] >= 0.5

print(
    "TEST 3 PASSED — valid response accepted"
)


# ============================================================
# TEST 4 — DESTINATION CONTRADICTION
# ============================================================

response = """
Here is a 5-day trip to Goa for 4 people.
"""

result = check_ai_output(
    response,
    workflow
)

assert result["valid"] is False

assert len(
    result["contradictions"]
) > 0

print(
    "TEST 4 PASSED — semantic destination contradiction detected"
)


# ============================================================
# TEST 5 — PEOPLE COUNT CONTRADICTION
# ============================================================

response = """
Here is a 5-day trip to Kerala for 8 people.
"""

result = check_ai_output(
    response,
    workflow
)

assert result["valid"] is False

assert len(
    result["contradictions"]
) > 0

print(
    "TEST 5 PASSED — semantic people-count contradiction detected"
)


# ============================================================
# TEST 6 — DURATION CONTRADICTION
# ============================================================

response = """
Here is a 10-day trip to Kerala for 4 people.
"""

result = check_ai_output(
    response,
    workflow
)

assert result["valid"] is False

assert len(
    result["contradictions"]
) > 0

print(
    "TEST 6 PASSED — semantic duration contradiction detected"
)


# ============================================================
# TEST 7 — ADDITIONAL INFORMATION
# ============================================================

response = """
Kerala is a beautiful destination.

Your five-day trip for four people could include:

Day 1: Kochi
Day 2: Munnar
Day 3: Thekkady
Day 4: Alleppey
Day 5: Kochi
"""

result = check_ai_output(
    response,
    workflow
)

assert result["valid"] is True

print(
    "TEST 7 PASSED — additional information accepted"
)


# ============================================================
# TEST 8 — UNCERTAIN RESPONSE
# ============================================================

response = """
You may want to consider Kerala or Goa.
The trip could potentially be five or seven days.
"""

result = check_ai_output(
    response,
    workflow
)

assert result["valid"] is False or len(
    result["issues"]
) > 0

print(
    "TEST 8 PASSED — uncertainty identified"
)


# ============================================================
# TEST 9 — USER VALUE MUST REMAIN AUTHORITATIVE
# ============================================================

response = """
I recommend changing the destination to Goa
because it may be cheaper.
"""

result = check_ai_output(
    response,
    workflow
)

assert result["valid"] is False

assert len(
    result["contradictions"]
) > 0 or len(
    result["issues"]
) > 0

print(
    "TEST 9 PASSED — user-confirmed value remains authoritative"
)


# ============================================================
# TEST 10 — NORMAL NATURAL LANGUAGE
# ============================================================

response = """
Based on your requirements, I recommend spending five
days exploring Kerala with your group of four people.
"""

result = check_ai_output(
    response,
    workflow
)

assert result["valid"] is True

print(
    "TEST 10 PASSED — natural language response validated"
)


# ============================================================
# FINAL
# ============================================================

print()
print(
    "ALL AI OUTPUT CHECKER TESTS PASSED"
)