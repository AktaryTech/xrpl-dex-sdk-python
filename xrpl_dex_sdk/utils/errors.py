from typing import Any


def handle_response_error(error_object: Any):
    if "error" in error_object:
        error: str = error_object["error"]
        if "error_message" in error_object:
            error_message: str = error_object["error_message"]
            raise Exception(error_message)
        raise Exception(error)


__all__ = ["handle_response_error"]
