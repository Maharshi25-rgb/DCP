from unittest.mock import patch

from models.generic_workflow import (
    GenericWorkflow,
    WorkflowField
)

from services.output_engine import (
    process_ai_output,
    MAX_AI_REPAIR_ATTEMPTS
)


# ============================================================
# TEST WORKFLOW
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


# ============================================================
# TEST 1 — VALID RESPONSE ACCEPTED
# ============================================================

with patch(
    "services.output_engine.check_ai_output"
) as mock_checker:

    mock_checker.return_value = {
        "valid": True,
        "confidence": 0.98,
        "issues": [],
        "contradictions": [],
        "unsupported_claims": [],
        "reasoning": "Response is consistent."
    }

    response = """
    Here is a 5-day trip to Kerala for 4 people.
    """

    result = process_ai_output(
        response,
        workflow
    )

    assert result["status"] == "accepted"

    assert result["repair_attempts"] == 0

print(
    "TEST 1 PASSED — valid response accepted"
)


# ============================================================
# TEST 2 — DETERMINISTIC FAILURE TRIGGERS REPAIR
# ============================================================

with patch(
    "services.output_engine.repair_ai_output"
) as mock_repair:

    mock_repair.return_value = {
        "success": True,
        "response": (
            "Here is a 5-day trip to Kerala "
            "for 4 people."
        ),
        "error": None
    }

    with patch(
        "services.output_engine.check_ai_output"
    ) as mock_checker:

        mock_checker.return_value = {
            "valid": True,
            "confidence": 0.98,
            "issues": [],
            "contradictions": [],
            "unsupported_claims": [],
            "reasoning": "Repaired response is valid."
        }

        response = """
        Here is a 10-day trip to Goa for 8 people.
        """

        result = process_ai_output(
            response,
            workflow
        )

        assert result["status"] == "accepted"

        assert result["repair_attempts"] == 1

        assert (
            result["response"]
            == mock_repair.return_value["response"]
        )

print(
    "TEST 2 PASSED — deterministic failure repaired"
)


# ============================================================
# TEST 3 — AI SEMANTIC FAILURE TRIGGERS REPAIR
# ============================================================

with patch(
    "services.output_engine.check_ai_output"
) as mock_checker:

    mock_checker.side_effect = [
        {
            "valid": False,
            "confidence": 0.30,
            "issues": [
                "Semantic inconsistency detected."
            ],
            "contradictions": [
                "Duration appears inconsistent."
            ],
            "unsupported_claims": [],
            "reasoning": "Response needs repair."
        },
        {
            "valid": True,
            "confidence": 0.95,
            "issues": [],
            "contradictions": [],
            "unsupported_claims": [],
            "reasoning": "Repaired response is consistent."
        }
    ]

    with patch(
        "services.output_engine.repair_ai_output"
    ) as mock_repair:

        mock_repair.return_value = {
            "success": True,
            "response": (
                "Here is a 5-day trip to Kerala "
                "for 4 people."
            ),
            "error": None
        }

        response = """
        Kerala trip for 4 people with inconsistent details.
        """

        result = process_ai_output(
            response,
            workflow
        )

        assert result["status"] == "accepted"

        assert result["repair_attempts"] == 1

print(
    "TEST 3 PASSED — semantic failure repaired"
)


# ============================================================
# TEST 4 — REPAIR FAILURE
# ============================================================

with patch(
    "services.output_engine.repair_ai_output"
) as mock_repair:

    mock_repair.return_value = {
        "success": False,
        "response": None,
        "error": "Model failed to generate repair."
    }

    response = """
    Here is a 10-day trip to Goa for 8 people.
    """

    result = process_ai_output(
        response,
        workflow
    )

    assert result["status"] == "failed"

    assert result["stage"] == "repair_failed"

    assert result["repair_attempts"] == 0

print(
    "TEST 4 PASSED — repair failure handled"
)


# ============================================================
# TEST 5 — REPAIR LIMIT
# ============================================================

with patch(
    "services.output_engine.repair_ai_output"
) as mock_repair:

    # Every repair produces another invalid response.

    mock_repair.return_value = {
        "success": True,
        "response": (
            "Here is a 10-day trip to Goa "
            "for 8 people."
        ),
        "error": None
    }

    response = """
    Here is a 10-day trip to Goa for 8 people.
    """

    result = process_ai_output(
        response,
        workflow
    )

    assert result["status"] == "failed"

    assert (
        result["stage"]
        == "repair_limit_exceeded"
    )

    assert (
        result["repair_attempts"]
        == MAX_AI_REPAIR_ATTEMPTS
    )

print(
    "TEST 5 PASSED — repair limit enforced"
)


# ============================================================
# TEST 6 — EMPTY RESPONSE
# ============================================================

result = process_ai_output(
    "",
    workflow
)

assert result["status"] == "failed"

assert result["stage"] in {
    "repair_failed",
    "repair_limit_exceeded"
}

print(
    "TEST 6 PASSED — empty response handled"
)


# ============================================================
# TEST 7 — NON-STRING RESPONSE
# ============================================================

result = process_ai_output(
    None,
    workflow
)

assert result["status"] == "failed"

assert result["stage"] in {
    "repair_failed",
    "repair_limit_exceeded"
}

print(
    "TEST 7 PASSED — non-string response handled"
)


# ============================================================
# TEST 8 — REPAIR COUNT STARTS AT ZERO
# ============================================================

with patch(
    "services.output_engine.check_ai_output"
) as mock_checker:

    mock_checker.return_value = {
        "valid": True,
        "confidence": 1.0,
        "issues": [],
        "contradictions": [],
        "unsupported_claims": [],
        "reasoning": "Valid."
    }

    result = process_ai_output(
        "Valid Kerala trip for 4 people.",
        workflow
    )

    assert result["repair_attempts"] == 0

print(
    "TEST 8 PASSED — repair counter starts at zero"
)


# ============================================================
# TEST 9 — WORKFLOW IS NOT MODIFIED
# ============================================================

original_destination = (
    workflow.fields[0].value
)

original_people = (
    workflow.fields[1].value
)

original_duration = (
    workflow.fields[2].value
)

with patch(
    "services.output_engine.repair_ai_output"
) as mock_repair:

    mock_repair.return_value = {
        "success": True,
        "response": (
            "Here is a 5-day trip to Kerala "
            "for 4 people."
        ),
        "error": None
    }

    with patch(
        "services.output_engine.check_ai_output"
    ) as mock_checker:

        mock_checker.return_value = {
            "valid": True,
            "confidence": 1.0,
            "issues": [],
            "contradictions": [],
            "unsupported_claims": [],
            "reasoning": "Valid."
        }

        process_ai_output(
            "Invalid response.",
            workflow
        )

assert workflow.fields[0].value == original_destination

assert workflow.fields[1].value == original_people

assert workflow.fields[2].value == original_duration

print(
    "TEST 9 PASSED — workflow remains immutable"
)


# ============================================================
# TEST 10 — FINAL RESPONSE IS REPAIRED RESPONSE
# ============================================================

repaired_response = (
    "FINAL REPAIRED RESPONSE: "
    "5-day Kerala trip for 4 people."
)

with patch(
    "services.output_engine.validate_ai_output"
) as mock_validator:

    with patch(
        "services.output_engine.repair_ai_output"
    ) as mock_repair:

        # First validation fails.
        # Second validation succeeds.

        mock_validator.side_effect = [
            {
                "valid": False,
                "errors": [
                    "Response contains a contradiction."
                ],
                "warnings": [],
                "checked_fields": [],
                "contradictions": [
                    {
                        "field_name": "destination",
                        "expected": "Kerala",
                        "detected": "Goa"
                    }
                ]
            },
            {
                "valid": True,
                "errors": [],
                "warnings": [],
                "checked_fields": [
                    "destination"
                ],
                "contradictions": []
            }
        ]

        mock_repair.return_value = {
            "success": True,
            "response": repaired_response,
            "error": None
        }

        with patch(
            "services.output_engine.check_ai_output"
        ) as mock_checker:

            mock_checker.return_value = {
                "valid": True,
                "confidence": 1.0,
                "issues": [],
                "contradictions": [],
                "unsupported_claims": [],
                "reasoning": "Response is valid."
            }

            result = process_ai_output(
                "Bad response.",
                workflow
            )

            assert result["status"] == "accepted"

            assert result["repair_attempts"] == 1

            assert result["response"] == repaired_response

            mock_repair.assert_called_once()

print(
    "TEST 10 PASSED — final response is repaired response"
)