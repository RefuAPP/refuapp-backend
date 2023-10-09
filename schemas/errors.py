from pydantic import BaseModel


class DetailResponseBody(BaseModel):
    detail: str


CONFLICT_RESPONSE = {
    409: {"description": "Error: Conflict", "model": DetailResponseBody}
}
