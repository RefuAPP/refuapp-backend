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

INVALID_REQUEST = {
    400: {"description": "Error: Invalid Request", "model": DetailResponseBody}
}

INTERNAL_SERVER_ERROR = {
    500: {
        "description": "NTP server is probably failing",
        "model": DetailResponseBody,
    }
}
