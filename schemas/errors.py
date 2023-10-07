from pydantic import BaseModel


class DetailResponseBody(BaseModel):
    detail: str


BAD_REQUEST_RESPONSE = {
    400: {"description": "Error: Bad Request", "model": DetailResponseBody}
}

CONFLICT_RESPONSE = {
    409: {"description": "Error: Conflict", "model": DetailResponseBody}
}
