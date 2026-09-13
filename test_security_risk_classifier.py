from services.security_risk_classifier import (
    classify_security_risk
)


# ============================================================
# TEST 1 — NORMAL REQUEST
# ============================================================

result = classify_security_risk(
    injection_detected=False,
    categories=[]
)

assert result["risk_level"] == "low"
assert result["action"] == "allow"

print("TEST 1 PASSED — normal request")


# ============================================================
# TEST 2 — INSTRUCTION OVERRIDE
# ============================================================

result = classify_security_risk(
    injection_detected=True,
    categories=[
        "instruction_override"
    ]
)

assert result["risk_level"] == "medium"
assert result["action"] == "block"

print("TEST 2 PASSED — instruction override")


# ============================================================
# TEST 3 — ROLE MANIPULATION
# ============================================================

result = classify_security_risk(
    injection_detected=True,
    categories=[
        "role_manipulation"
    ]
)

assert result["risk_level"] == "medium"
assert result["action"] == "block"

print("TEST 3 PASSED — role manipulation")


# ============================================================
# TEST 4 — SYSTEM PROMPT EXTRACTION
# ============================================================

result = classify_security_risk(
    injection_detected=True,
    categories=[
        "system_prompt_extraction"
    ]
)

assert result["risk_level"] == "high"
assert result["action"] == "block"

print("TEST 4 PASSED — system prompt extraction")


# ============================================================
# TEST 5 — INTERNAL INFORMATION EXTRACTION
# ============================================================

result = classify_security_risk(
    injection_detected=True,
    categories=[
        "internal_information_extraction"
    ]
)

assert result["risk_level"] == "high"
assert result["action"] == "block"

print("TEST 5 PASSED — internal information extraction")


# ============================================================
# TEST 6 — MULTIPLE CATEGORIES
# ============================================================

result = classify_security_risk(
    injection_detected=True,
    categories=[
        "instruction_override",
        "system_prompt_extraction"
    ]
)

assert result["risk_level"] == "high"
assert result["action"] == "block"

print("TEST 6 PASSED — highest risk selected")


# ============================================================
# TEST 7 — UNKNOWN CATEGORY
# ============================================================

result = classify_security_risk(
    injection_detected=True,
    categories=[
        "unknown_security_category"
    ]
)

assert result["risk_level"] == "high"
assert result["action"] == "block"

print("TEST 7 PASSED — unknown category handled safely")


# ============================================================
# TEST 8 — MEDIUM + HIGH
# ============================================================

result = classify_security_risk(
    injection_detected=True,
    categories=[
        "role_manipulation",
        "internal_information_extraction"
    ]
)

assert result["risk_level"] == "high"
assert result["action"] == "block"

print("TEST 8 PASSED — mixed risk levels")


print()
print("ALL SECURITY RISK CLASSIFIER TESTS PASSED")