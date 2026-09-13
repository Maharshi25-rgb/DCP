from services.trusted_user_context import (
    build_trusted_user_context,
    is_user_confirmed
)


# ============================================================
# TEST 1 — USER PROVIDED VALUE
# ============================================================

result = build_trusted_user_context(
    {
        "destination": "Kerala",
        "number_of_people": 4
    }
)

assert result["valid"] is True

assert result["confirmed_fields"] == {
    "destination": "Kerala",
    "number_of_people": 4
}

print("TEST 1 PASSED — user values stored")


# ============================================================
# TEST 2 — CHECK CONFIRMED VALUE
# ============================================================

context = build_trusted_user_context(
    {
        "destination": "Kerala"
    }
)

assert is_user_confirmed(
    context,
    "destination",
    "Kerala"
) is True

print("TEST 2 PASSED — confirmed value recognized")


# ============================================================
# TEST 3 — AI INVENTED VALUE
# ============================================================

context = build_trusted_user_context(
    {
        "destination": "Kerala"
    }
)

assert is_user_confirmed(
    context,
    "budget",
    500000
) is False

print("TEST 3 PASSED — invented value rejected")


# ============================================================
# TEST 4 — WRONG VALUE
# ============================================================

context = build_trusted_user_context(
    {
        "destination": "Kerala"
    }
)

assert is_user_confirmed(
    context,
    "destination",
    "Goa"
) is False

print("TEST 4 PASSED — incorrect value rejected")


# ============================================================
# TEST 5 — NONE VALUE
# ============================================================

result = build_trusted_user_context(
    {
        "destination": None
    }
)

assert result["valid"] is True
assert result["confirmed_fields"] == {}

print("TEST 5 PASSED — None not treated as confirmation")


# ============================================================
# TEST 6 — EMPTY FIELD NAME
# ============================================================

result = build_trusted_user_context(
    {
        "": "Kerala"
    }
)

assert result["valid"] is True
assert result["confirmed_fields"] == {}

print("TEST 6 PASSED — empty field ignored")


# ============================================================
# TEST 7 — NON-DICTIONARY INPUT
# ============================================================

result = build_trusted_user_context(
    ["Kerala"]
)

assert result["valid"] is False
assert result["confirmed_fields"] == {}

print("TEST 7 PASSED — invalid input rejected")


# ============================================================
# TEST 8 — MULTIPLE USER VALUES
# ============================================================

context = build_trusted_user_context(
    {
        "destination": "Kerala",
        "number_of_people": 4,
        "trip_duration_days": 5,
        "budget": 50000
    }
)

assert is_user_confirmed(
    context,
    "destination",
    "Kerala"
)

assert is_user_confirmed(
    context,
    "number_of_people",
    4
)

assert is_user_confirmed(
    context,
    "trip_duration_days",
    5
)

assert is_user_confirmed(
    context,
    "budget",
    50000
)

print("TEST 8 PASSED — multiple values confirmed")


# ============================================================
# TEST 9 — UNCONFIRMED FIELD
# ============================================================

context = build_trusted_user_context(
    {
        "destination": "Kerala"
    }
)

assert is_user_confirmed(
    context,
    "number_of_people",
    4
) is False

print("TEST 9 PASSED — unconfirmed field rejected")


# ============================================================
# TEST 10 — SAME FIELD DIFFERENT VALUE
# ============================================================

context = build_trusted_user_context(
    {
        "budget": 50000
    }
)

assert is_user_confirmed(
    context,
    "budget",
    50000
) is True

assert is_user_confirmed(
    context,
    "budget",
    100000
) is False

print("TEST 10 PASSED — exact value matching")


# ============================================================
# FINAL
# ============================================================

print()
print("ALL TRUSTED USER CONTEXT TESTS PASSED")