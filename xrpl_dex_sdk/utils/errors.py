from typing import Any


def handle_response_error(error_object: Any):
    """Evaluates a response object and throws any errors found."""

    if "error" in error_object:
        error: str = error_object["error"]
        if "error_message" in error_object:
            error_message: str = error_object["error_message"]
            raise Exception(error_message)
        raise Exception(error)
