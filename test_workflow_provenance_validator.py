from models.generic_workflow import (
    GenericWorkflow,
    WorkflowField
)

from services.workflow_provenance_validator import (
    validate_workflow_provenance
)

from models.generic_workflow import (
    GenericWorkflow,
    WorkflowField,
    WorkflowSuggestion
)
# ============================================================
# TEST 1 — VALID USER CONFIRMED VALUE
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
            question="Where do you want to travel?",
            source="user_confirmed"
        )
    ],
    next_action="generate_prompt"
)

trusted_context = {
    "confirmed_fields": {
        "destination": "Kerala"
    }
}

result = validate_workflow_provenance(
    workflow,
    trusted_context
)

assert result["valid"] is True

print(
    "TEST 1 PASSED — valid user-confirmed value"
)


# ============================================================
# TEST 2 — AI CANNOT CLAIM USER CONFIRMATION
# ============================================================

workflow = GenericWorkflow(
    workflow_type="travel_planning",
    user_request="Plan a trip to Kerala",
    fields=[
        WorkflowField(
            field_name="budget",
            value="500000",
            field_type="integer",
            required=False,
            question="What is your budget?",
            source="user_confirmed"
        )
    ],
    next_action="generate_prompt"
)

trusted_context = {
    "confirmed_fields": {}
}

result = validate_workflow_provenance(
    workflow,
    trusted_context
)

assert result["valid"] is False

print(
    "TEST 2 PASSED — AI cannot claim user confirmation"
)


# ============================================================
# TEST 3 — AI-INVENTED VALUE DOES NOT MATCH USER VALUE
# ============================================================

workflow = GenericWorkflow(
    workflow_type="travel_planning",
    user_request="Plan a trip to Kerala",
    fields=[
        WorkflowField(
            field_name="budget",
            value="500000",
            field_type="integer",
            required=False,
            question="What is your budget?",
            source="user_confirmed"
        )
    ],
    next_action="generate_prompt"
)

trusted_context = {
    "confirmed_fields": {
        "budget": "50000"
    }
}

result = validate_workflow_provenance(
    workflow,
    trusted_context
)

assert result["valid"] is False

print(
    "TEST 3 PASSED — mismatched user value blocked"
)


# ============================================================
# TEST 4 — USER VALUE MATCHES EXACTLY
# ============================================================

workflow = GenericWorkflow(
    workflow_type="travel_planning",
    user_request="Plan a trip",
    fields=[
        WorkflowField(
            field_name="budget",
            value="50000",
            field_type="integer",
            required=False,
            question="What is your budget?",
            source="user_confirmed"
        )
    ],
    next_action="generate_prompt"
)

trusted_context = {
    "confirmed_fields": {
        "budget": "50000"
    }
}

result = validate_workflow_provenance(
    workflow,
    trusted_context
)

assert result["valid"] is True

print(
    "TEST 4 PASSED — exact user value accepted"
)


# ============================================================
# TEST 5 — MISSING FIELD MUST BE MISSING
# ============================================================

workflow = GenericWorkflow(
    workflow_type="travel_planning",
    user_request="Plan a trip",
    fields=[
        WorkflowField(
            field_name="budget",
            value=None,
            field_type="integer",
            required=False,
            question="What is your budget?",
            source="missing"
        )
    ],
    next_action="collect_information"
)

result = validate_workflow_provenance(
    workflow
)

assert result["valid"] is True

print(
    "TEST 5 PASSED — missing field provenance"
)


# ============================================================
# TEST 6 — VALUE CANNOT BE MARKED MISSING
# ============================================================

workflow = GenericWorkflow(
    workflow_type="travel_planning",
    user_request="Plan a trip",
    fields=[
        WorkflowField(
            field_name="budget",
            value="50000",
            field_type="integer",
            required=False,
            question="What is your budget?",
            source="missing"
        )
    ],
    next_action="generate_prompt"
)

result = validate_workflow_provenance(
    workflow
)

assert result["valid"] is False

print(
    "TEST 6 PASSED — value marked missing blocked"
)


# ============================================================
# TEST 7 — AI SUGGESTED VALUE IS ALLOWED
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
            question="Where do you want to travel?",
            source="user_confirmed"
        )
    ],
    next_action="generate_prompt"
)

workflow.suggestions.append(
    WorkflowSuggestion(
        field_name="budget",
        value="50000",
        reason="Suitable estimated budget",
        status="pending_confirmation"
    )
)

result = validate_workflow_provenance(
    workflow,
    {
        "confirmed_fields": {
            "destination": "Kerala"
        }
    }
)

assert result["valid"] is True

print(
    "TEST 7 PASSED — AI suggestion remains untrusted"
)


# ============================================================
# FINAL
# ============================================================

print()
print(
    "ALL PROVENANCE ENFORCEMENT TESTS PASSED"
)