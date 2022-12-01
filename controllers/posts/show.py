from typing import Tuple, Any


def get(request) -> tuple[Any, str]:  # in future will be using id
    return request.accepts, "html"
