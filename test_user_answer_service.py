from services.user_answer_service import (
    capture_user_answers
)

from services.trusted_user_context import (
    is_user_confirmed
)


# ============================================================
# TEST 1 — CAPTURE USER ANSWER
# ============================================================

result = capture_user_answers(
    {
        "destination": "Kerala"
    }
)

assert result["valid"] is True

assert is_user_confirmed(
    result["trusted_context"],
    "destination",
    "Kerala"
) is True

print("TEST 1 PASSED — user answer captured")


# ============================================================
# TEST 2 — MULTIPLE USER ANSWERS
# ============================================================

result = capture_user_answers(
    {
        "destination": "Kerala",
        "number_of_people": 4,
        "trip_duration_days": 5
    }
)

assert result["valid"] is True

assert is_user_confirmed(
    result["trusted_context"],
    "destination",
    "Kerala"
) is True

assert is_user_confirmed(
    result["trusted_context"],
    "number_of_people",
    4
) is True

assert is_user_confirmed(
    result["trusted_context"],
    "trip_duration_days",
    5
) is True

print("TEST 2 PASSED — multiple answers captured")


# ============================================================
# TEST 3 — AI-INVENTED VALUE NOT PRESENT
# ============================================================

result = capture_user_answers(
    {
        "destination": "Kerala"
    }
)

assert is_user_confirmed(
    result["trusted_context"],
    "budget",
    500000
) is False

print("TEST 3 PASSED — AI-invented value not trusted")


# ============================================================
# TEST 4 — WRONG VALUE NOT TRUSTED
# ============================================================

result = capture_user_answers(
    {
        "destination": "Kerala"
    }
)

assert is_user_confirmed(
    result["trusted_context"],
    "destination",
    "Goa"
) is False

print("TEST 4 PASSED — incorrect value not trusted")


# ============================================================
# TEST 5 — NONE IS NOT CONFIRMED
# ============================================================

result = capture_user_answers(
    {
        "destination": None
    }
)

assert result["valid"] is True

assert is_user_confirmed(
    result["trusted_context"],
    "destination",
    None
) is False

print("TEST 5 PASSED — None not trusted")


# ============================================================
# TEST 6 — INVALID INPUT TYPE
# ============================================================

result = capture_user_answers(
    ["Kerala"]
)

assert result["valid"] is False

print("TEST 6 PASSED — invalid input rejected")


# ============================================================
# TEST 7 — EMPTY ANSWERS
# ============================================================

result = capture_user_answers({})

assert result["valid"] is True

assert result["trusted_context"][
    "confirmed_fields"
] == {}

print("TEST 7 PASSED — empty answer set handled")


# ============================================================
# TEST 8 — EXACT VALUE REQUIRED
# ============================================================

result = capture_user_answers(
    {
        "budget": 50000
    }
)

assert is_user_confirmed(
    result["trusted_context"],
    "budget",
    50000
) is True

assert is_user_confirmed(
    result["trusted_context"],
    "budget",
    50001
) is False

print("TEST 8 PASSED — exact user value required")


# ============================================================
# FINAL
# ============================================================

print()
print("ALL USER ANSWER SERVICE TESTS PASSED")