from models.generic_workflow import (
    GenericWorkflow,
    WorkflowField
)

from services.workflow_engine import (
    process_workflow
)

from services.prompt_service import (
    build_prompt
)

from services.output_engine import (
    process_ai_output
)


# ============================================================
# TEST WORKFLOW
# ============================================================

workflow = GenericWorkflow(

    workflow_type="travel_planning",

    user_request=(
        "Plan a 5-day trip to Kerala for 4 people "
        "starting on 2026-10-01 with a budget of 40000."
    ),

    fields=[

        # ----------------------------------------------------
        # DESTINATION
        # ----------------------------------------------------

        WorkflowField(
            field_name="destination",
            value="Kerala",
            field_type="string",
            required=True,
            question="Where do you want to travel?",
            source="user_confirmed"
        ),

        # ----------------------------------------------------
        # START DATE
        # ----------------------------------------------------

        WorkflowField(
            field_name="start_date",
            value="2026-10-01",
            field_type="date",
            required=True,
            question="When does the trip start?",
            source="user_confirmed"
        ),

        # ----------------------------------------------------
        # TRIP DURATION
        # ----------------------------------------------------

        WorkflowField(
            field_name="trip_duration_days",
            value="5",
            field_type="integer",
            required=True,
            question="How many days will the trip be?",
            source="user_confirmed"
        ),

        # ----------------------------------------------------
        # NUMBER OF PEOPLE
        # ----------------------------------------------------

        WorkflowField(
            field_name="number_of_people",
            value="4",
            field_type="integer",
            required=True,
            question="How many people are travelling?",
            source="user_confirmed"
        ),

        # ----------------------------------------------------
        # BUDGET
        # ----------------------------------------------------

        WorkflowField(
            field_name="budget",
            value="40000",
            field_type="integer",
            required=False,
            question="What is your budget?",
            source="user_confirmed"
        )
    ],

    suggestions=[],

    next_action="generate_prompt"
)


# ============================================================
# TRUSTED USER CONTEXT
# ============================================================

trusted_context = {

    "confirmed_fields": {

        "destination": "Kerala",

        "start_date": "2026-10-01",

        "trip_duration_days": "5",

        "number_of_people": "4",

        "budget": "40000"
    }
}


# ============================================================
# MOCK AI RESPONSE
# ============================================================

mock_ai_response = (
    "Here is a 5-day Kerala travel plan for 4 people "
    "starting on 2026-10-01 within a budget of 40000."
)


# ============================================================
# TEST 1 — WORKFLOW ENGINE
# ============================================================

result = process_workflow(
    workflow,
    trusted_user_context=trusted_context
)

assert result["status"] == "valid"

assert result["workflow"].workflow_type == (
    "travel_planning"
)

assert result["evaluation"]["status"] == "complete"

assert result["evaluation"]["next_action"] == (
    "generate_prompt"
)

print(
    "TEST 1 PASSED — workflow engine"
)


# ============================================================
# TEST 2 — INPUT SECURITY
# ============================================================

assert result["security"]["secure"] is True

assert result["security"]["decision"] == "allow"

assert result["security"]["injection_detected"] is False

print(
    "TEST 2 PASSED — input security"
)


# ============================================================
# TEST 3 — PROVENANCE VALIDATION
# ============================================================

assert result[
    "provenance_validation"
]["valid"] is True

print(
    "TEST 3 PASSED — trusted provenance"
)


# ============================================================
# TEST 4 — FIELD VALUE VALIDATION
# ============================================================

assert result[
    "field_value_validation"
]["valid"] is True

print(
    "TEST 4 PASSED — field value validation"
)


# ============================================================
# TEST 5 — WORKFLOW IS COMPLETE
# ============================================================

evaluation = result["evaluation"]

assert evaluation["status"] == "complete"

assert evaluation["next_action"] == (
    "generate_prompt"
)

assert evaluation["missing_required_fields"] == []

print(
    "TEST 5 PASSED — workflow evaluation"
)


# ============================================================
# TEST 6 — NORMALIZATION
# ============================================================

normalized_workflow = result["workflow"]

assert normalized_workflow.workflow_type == (
    "travel_planning"
)

assert normalized_workflow.fields[0].field_name == (
    "destination"
)

assert normalized_workflow.fields[1].field_name == (
    "start_date"
)

assert normalized_workflow.fields[2].field_name == (
    "trip_duration_days"
)

assert normalized_workflow.fields[3].field_name == (
    "number_of_people"
)

assert normalized_workflow.fields[4].field_name == (
    "budget"
)

print(
    "TEST 6 PASSED — workflow normalization"
)


# ============================================================
# TEST 7 — PROMPT BUILDER
# ============================================================

prompt_result = build_prompt(
    workflow
)

assert isinstance(
    prompt_result,
    str
)

assert len(prompt_result.strip()) > 0

assert "Kerala" in prompt_result

assert "2026-10-01" in prompt_result

assert "5" in prompt_result

assert "4" in prompt_result

assert "40000" in prompt_result

print(
    "TEST 7 PASSED — prompt builder"
)


# ============================================================
# TEST 8 — OUTPUT ENGINE
# ============================================================

output_result = process_ai_output(
    mock_ai_response,
    workflow
)

assert output_result["status"] == (
    "accepted"
)

assert output_result["stage"] == (
    "output_validation_complete"
)

assert output_result["response"] == (
    mock_ai_response
)

print(
    "TEST 8 PASSED — output engine"
)


# ============================================================
# TEST 9 — NO REPAIR REQUIRED
# ============================================================

assert output_result[
    "repair_attempts"
] == 0

assert output_result[
    "deterministic_validation"
]["valid"] is True

assert output_result[
    "ai_check"
]["valid"] is True

print(
    "TEST 9 PASSED — no unnecessary repair"
)


# ============================================================
# TEST 10 — WORKFLOW IMMUTABILITY
# ============================================================

assert workflow.fields[0].value == (
    "Kerala"
)

assert workflow.fields[1].value == (
    "2026-10-01"
)

assert workflow.fields[2].value == (
    "5"
)

assert workflow.fields[3].value == (
    "4"
)

assert workflow.fields[4].value == (
    "40000"
)

print(
    "TEST 10 PASSED — workflow remained immutable"
)


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 65)
print("DCP FULL PIPELINE TEST PASSED")
print("=" * 65)

print()
print("Input Security         : PASS")
print("Workflow Engine        : PASS")
print("Provenance             : PASS")
print("Normalization          : PASS")
print("Structure Validation   : PASS")
print("Field Validation       : PASS")
print("Workflow Evaluation    : PASS")
print("Prompt Builder         : PASS")
print("Deterministic Output   : PASS")
print("AI Semantic Checker    : PASS")
print("Output Engine          : PASS")
print("Repair Attempts        : 0")
print("Workflow Immutability  : PASS")

print()
print("DCP CORE PIPELINE      : READY")
print("=" * 65)