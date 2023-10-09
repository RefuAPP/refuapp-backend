from pydantic import BaseModel


class DetailResponseBody(BaseModel):
    detail: str


CONFLICT_RESPONSE = {
    409: {"description": "Error: Conflict", "model": DetailResponseBody}
}

NOT_FOUND_RESPONSE = {
    404: {"description": "Error: Not Found", "model": DetailResponseBody}
}

UNAUTHORIZED_RESPONSE = {
    401: {"description": "Error: Unauthorized", "model": DetailResponseBody}
}

FORBIDDEN_RESPONSE = {
    403: {"description": "Error: Forbidden", "model": DetailResponseBody}
}
