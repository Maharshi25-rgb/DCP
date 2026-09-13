from typing import Any


def build_trusted_user_context(
    user_answers: dict[str, Any]
):
    """
    Build trusted context from explicitly supplied user answers.
    """

    if not isinstance(user_answers, dict):
        return {
            "valid": False,
            "errors": [
                "User answers must be a dictionary."
            ],
            "confirmed_fields": {}
        }

    confirmed_fields = {}

    for field_name, value in user_answers.items():

        if not isinstance(field_name, str):
            continue

        if not field_name.strip():
            continue

        if value is None:
            continue

        confirmed_fields[field_name] = value

    return {
        "valid": True,
        "errors": [],
        "confirmed_fields": confirmed_fields
    }


def is_user_confirmed(
    trusted_context: dict,
    field_name: str,
    value: Any
) -> bool:
    """
    Compare values using normalized string representation.
    """

    if not isinstance(trusted_context, dict):
        return False

    confirmed_fields = trusted_context.get(
        "confirmed_fields",
        {}
    )

    if not isinstance(confirmed_fields, dict):
        return False

    if field_name not in confirmed_fields:
        return False

    return str(confirmed_fields[field_name]) == str(value)
