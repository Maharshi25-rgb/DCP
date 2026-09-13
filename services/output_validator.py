from typing import Any
import re
from datetime import datetime

from models.generic_workflow import GenericWorkflow


# ============================================================
# NORMALIZATION HELPERS
# ============================================================

def normalize_text(value: Any) -> str:
    """
    Normalize text for comparison.
    """

    return str(value).strip().lower()


def normalize_date(value: Any) -> str | None:
    """
    Convert common date formats into YYYY-MM-DD.

    Supported formats:

        2026-10-01
        2026/10/01
        October 1, 2026
        Oct 1, 2026
        1 October 2026
        1 Oct 2026
    """

    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    supported_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d %B %Y",
        "%d %b %Y",
    ]

    for date_format in supported_formats:
        try:
            parsed_date = datetime.strptime(
                text,
                date_format
            )

            return parsed_date.strftime("%Y-%m-%d")

        except ValueError:
            continue

    return None


def date_is_present(
    expected_value: Any,
    response: str
) -> bool:
    """
    Check whether the expected date appears in the response
    using any supported date format.
    """

    expected_date = normalize_date(expected_value)

    if expected_date is None:
        return normalize_text(expected_value) in response

    parsed_date = datetime.strptime(
        expected_date,
        "%Y-%m-%d"
    )

    possible_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d %B %Y",
        "%d %b %Y",
    ]

    for date_format in possible_formats:

        formatted_date = parsed_date.strftime(
            date_format
        ).lower()

        if formatted_date in response:
            return True

    return False


# ============================================================
# OUTPUT VALIDATOR
# ============================================================

def validate_ai_output(
    ai_response: Any,
    workflow: GenericWorkflow
):
    """
    Validate an AI-generated response against the workflow.

    V1 responsibilities:

        1. Validate response type
        2. Validate response is not empty
        3. Check user-confirmed values
        4. Detect direct contradictions
        5. Normalize date-format comparisons
        6. Return structured validation results

    This validator checks workflow consistency.
    It does not verify every factual statement made by the AI.
    """

    errors = []
    warnings = []
    checked_fields = []
    contradictions = []

    # ========================================================
    # CHECK 1 — RESPONSE TYPE
    # ========================================================

    if not isinstance(ai_response, str):

        return {
            "valid": False,
            "errors": [
                "AI response must be a string."
            ],
            "warnings": [],
            "checked_fields": [],
            "contradictions": []
        }

    # ========================================================
    # CHECK 2 — EMPTY RESPONSE
    # ========================================================

    if not ai_response.strip():

        return {
            "valid": False,
            "errors": [
                "AI response cannot be empty."
            ],
            "warnings": [],
            "checked_fields": [],
            "contradictions": []
        }

    normalized_response = normalize_text(ai_response)

    # ========================================================
    # CHECK 3 — USER-CONFIRMED VALUES
    # ========================================================

    for field in workflow.fields:

        if field.source != "user_confirmed":
            continue

        if field.value is None:
            continue

        checked_fields.append(
            field.field_name
        )

        expected_value = normalize_text(
            field.value
        )

        if not expected_value:
            continue

        # ====================================================
        # DATE VALIDATION
        # ====================================================

        if field.field_type == "date":

            if not date_is_present(
                field.value,
                normalized_response
            ):

                warnings.append(
                    f"User-confirmed date field "
                    f"'{field.field_name}' with value "
                    f"'{field.value}' was not explicitly "
                    "found in the AI response."
                )

            # Do not run the generic text comparison
            # for dates because the AI may use another
            # valid date format.
            continue

        # ====================================================
        # DESTINATION VALIDATION
        # ====================================================

        if field.field_name == "destination":

            common_destinations = {
                "kerala",
                "goa",
                "hyderabad",
                "mumbai",
                "delhi",
                "bangalore",
                "chennai",
                "kolkata",
                "pune",
                "rajasthan",
                "karnataka",
                "tamil nadu"
            }

            detected_destinations = [
                destination
                for destination in common_destinations
                if destination in normalized_response
            ]

            for detected in detected_destinations:

                if detected != expected_value:

                    contradictions.append({
                        "field_name": field.field_name,
                        "expected": field.value,
                        "detected": detected
                    })

                    errors.append(
                        f"AI response contradicts "
                        f"user-confirmed "
                        f"{field.field_name}: expected "
                        f"'{field.value}', detected "
                        f"'{detected}'."
                    )

        # ====================================================
        # NUMBER OF PEOPLE VALIDATION
        # ====================================================

        if field.field_name == "number_of_people":

            numbers = re.findall(
                r"\b\d+\b",
                normalized_response
            )

            for number in numbers:

                if number == expected_value:
                    continue

                contradiction_phrases = [
                    f"{number} people",
                    f"{number} person",
                    f"for {number}"
                ]

                if any(
                    phrase in normalized_response
                    for phrase in contradiction_phrases
                ):

                    contradictions.append({
                        "field_name": field.field_name,
                        "expected": field.value,
                        "detected": number
                    })

                    errors.append(
                        f"AI response may contradict "
                        f"user-confirmed "
                        f"{field.field_name}: expected "
                        f"'{field.value}', detected "
                        f"'{number}'."
                    )

        # ====================================================
        # TRIP DURATION VALIDATION
        # ====================================================

        if field.field_name == "trip_duration_days":

            duration_matches = re.findall(
                r"\b(\d+)[ -]day",
                normalized_response
            )

            for number in duration_matches:

                if number == expected_value:
                    continue

                contradictions.append({
                    "field_name": field.field_name,
                    "expected": field.value,
                    "detected": number
                })

                errors.append(
                    f"AI response may contradict "
                    f"user-confirmed "
                    f"{field.field_name}: expected "
                    f"'{field.value}', detected "
                    f"'{number}'."
                )

                # ====================================================
        # GENERAL VALUE PRESENCE CHECK
        # ====================================================

        expected_present = (
            expected_value in normalized_response
        )

        # Boolean values are commonly expressed naturally
        # rather than as the literal strings "true" or "false".
        if field.field_type == "boolean":

            boolean_value = str(field.value).strip().lower()

            if boolean_value == "true":
                boolean_phrases = [
                    "before it expires",
                    "before expiry",
                    "before expiration",
                    "renew before expiry",
                    "renew before expiration",
                    "renewed before expiry",
                    "renewed before expiration",
                    "enable renewal",
                    "automatic renewal",
                    "auto renewal",
                    "renewal is required",
                    "renewal should be performed"
                ]

                expected_present = (
                    expected_present
                    or any(
                        phrase in normalized_response
                        for phrase in boolean_phrases
                    )
                )

            elif boolean_value == "false":
                boolean_phrases = [
                    "do not renew",
                    "don't renew",
                    "not renew",
                    "renewal is not required",
                    "automatic renewal is disabled",
                    "auto renewal is disabled"
                ]

                expected_present = (
                    expected_present
                    or any(
                        phrase in normalized_response
                        for phrase in boolean_phrases
                    )
                )

        if not expected_present:

            warnings.append(
                f"User-confirmed field "
                f"'{field.field_name}' with value "
                f"'{field.value}' was not explicitly "
                "found in the AI response."
            )
    # ========================================================
    # FINAL RESULT
    # ========================================================

    if contradictions:

        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings,
            "checked_fields": checked_fields,
            "contradictions": contradictions
        }

    return {
        "valid": True,
        "errors": [],
        "warnings": warnings,
        "checked_fields": checked_fields,
        "contradictions": []
    }