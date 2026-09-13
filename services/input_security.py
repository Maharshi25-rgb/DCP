from typing import Any


MAX_USER_REQUEST_LENGTH = 10000


def validate_user_input(
    user_request: Any
):
    """
    Validate the basic security boundaries of a user request.

    This layer checks input shape and size only.
    It does not attempt to determine whether the
    user's request is malicious.
    """

    errors = []

    # =========================================
    # TYPE CHECK
    # =========================================

    if not isinstance(user_request, str):

        errors.append(
            "User request must be a string."
        )

        return {
            "valid": False,
            "errors": errors
        }

    # =========================================
    # EMPTY INPUT
    # =========================================

    if not user_request.strip():

        errors.append(
            "User request cannot be empty."
        )

    # =========================================
    # INPUT SIZE
    # =========================================

    if len(user_request) > MAX_USER_REQUEST_LENGTH:

        errors.append(
            f"User request exceeds the maximum "
            f"allowed length of "
            f"{MAX_USER_REQUEST_LENGTH} characters."
        )

    # =========================================
    # RESULT
    # =========================================

    if errors:

        return {
            "valid": False,
            "errors": errors
        }

    return {
        "valid": True,
        "errors": []
    }