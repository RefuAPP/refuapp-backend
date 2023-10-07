from pydantic import BaseModel


class BadRequest(BaseModel):
    detail: str


BAD_REQUEST_RESPONSE = {
    400: {"description": "Error: Bad Request", "model": BadRequest}
}

CONFLICT_RESPONSE = {
    409: {"description": "Error: Conflict", "model": BadRequest}
}
