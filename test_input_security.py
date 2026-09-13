from services.input_security import (
    validate_user_input,
    MAX_USER_REQUEST_LENGTH
)


# =========================================
# TEST 1 — VALID INPUT
# =========================================

result = validate_user_input(
    "Plan a 5 day trip to Kerala."
)

print("\nTEST 1 — VALID INPUT")
print(result)

assert result["valid"] is True
assert result["errors"] == []


# =========================================
# TEST 2 — EMPTY INPUT
# =========================================

result = validate_user_input("")

print("\nTEST 2 — EMPTY INPUT")
print(result)

assert result["valid"] is False
assert "cannot be empty" in result["errors"][0]


# =========================================
# TEST 3 — WHITESPACE INPUT
# =========================================

result = validate_user_input("     ")

print("\nTEST 3 — WHITESPACE INPUT")
print(result)

assert result["valid"] is False


# =========================================
# TEST 4 — NON-STRING INPUT
# =========================================

result = validate_user_input(12345)

print("\nTEST 4 — NON-STRING INPUT")
print(result)

assert result["valid"] is False
assert "must be a string" in result["errors"][0]


# =========================================
# TEST 5 — MAXIMUM LENGTH
# =========================================

valid_input = "A" * MAX_USER_REQUEST_LENGTH

result = validate_user_input(valid_input)

print("\nTEST 5 — MAXIMUM LENGTH")
print(result)

assert result["valid"] is True


# =========================================
# TEST 6 — ABOVE MAXIMUM LENGTH
# =========================================

invalid_input = (
    "A" * (MAX_USER_REQUEST_LENGTH + 1)
)

result = validate_user_input(invalid_input)

print("\nTEST 6 — ABOVE MAXIMUM LENGTH")
print(result)

assert result["valid"] is False

assert any(
    "exceeds the maximum" in error
    for error in result["errors"]
)


# =========================================
# FINAL
# =========================================

print(
    "\nALL INPUT SECURITY TESTS PASSED"
)