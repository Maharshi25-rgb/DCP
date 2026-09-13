from datetime import datetime
from typing import Any


ALLOWED_FIELD_TYPES = {
    "string",
    "integer",
    "boolean",
    "date",
    "list",
    "enum",
}


def validate_field_value(
    value: Any,
    field_type: str
):
    """
    Validate a field value against its expected field type.
    """

    # -----------------------------------------
    # 1. Validate field type
    # -----------------------------------------

    if field_type not in ALLOWED_FIELD_TYPES:

        return {
            "valid": False,
            "error": f"Unsupported field type: '{field_type}'"
        }

    # -----------------------------------------
    # 2. Handle missing value
    # -----------------------------------------

    if value is None:

        return {
            "valid": True,
            "error": None
        }

    # -----------------------------------------
    # 3. String
    # -----------------------------------------

    if field_type == "string":

        if isinstance(value, str) and value.strip():

            return {
                "valid": True,
                "error": None
            }

        return {
            "valid": False,
            "error": "Value must be a non-empty string."
        }

    # -----------------------------------------
    # 4. Integer
    # -----------------------------------------

    if field_type == "integer":

        if isinstance(value, bool):

            return {
                "valid": False,
                "error": "Boolean values are not valid integers."
            }

        if isinstance(value, int):

            return {
                "valid": True,
                "error": None
            }

        if isinstance(value, str):

            try:
                int(value.strip())

                return {
                    "valid": True,
                    "error": None
                }

            except ValueError:
                pass

        return {
            "valid": False,
            "error": "Value must be an integer."
        }

    # -----------------------------------------
    # 5. Boolean
    # -----------------------------------------

    if field_type == "boolean":

        if isinstance(value, bool):

            return {
                "valid": True,
                "error": None
            }

        if isinstance(value, str):

            normalized_value = value.strip().lower()

            if normalized_value in {
                "true",
                "false"
            }:

                return {
                    "valid": True,
                    "error": None
                }

        return {
            "valid": False,
            "error": "Value must be true or false."
        }

    # -----------------------------------------
    # 6. Date
    # -----------------------------------------

    if field_type == "date":

        if isinstance(value, datetime):

            return {
                "valid": True,
                "error": None
            }

        if isinstance(value, str):

            try:
                datetime.strptime(
                    value.strip(),
                    "%Y-%m-%d"
                )

                return {
                    "valid": True,
                    "error": None
                }

            except ValueError:
                pass

        return {
            "valid": False,
            "error": "Date must use YYYY-MM-DD format."
        }

    # -----------------------------------------
    # 7. List
    # -----------------------------------------

    if field_type == "list":

        if isinstance(value, list) and len(value) > 0:

            return {
                "valid": True,
                "error": None
            }

        if isinstance(value, str):

            items = [
                item.strip()
                for item in value.split(",")
                if item.strip()
            ]

            if items:

                return {
                    "valid": True,
                    "error": None
                }

        return {
            "valid": False,
            "error": "Value must be a non-empty list."
        }

    # -----------------------------------------
    # 8. Enum
    # -----------------------------------------

    if field_type == "enum":

        if isinstance(value, str) and value.strip():

            return {
                "valid": True,
                "error": None
            }

        return {
            "valid": False,
            "error": "Enum value must be a non-empty string."
        }

    return {
        "valid": False,
        "error": "Unknown validation error."
    }