from pydantic import BaseModel


class DetailResponseBody(BaseModel):
    detail: str


CONFLICT_RESPONSE = {
    409: {"description": "Error: Conflict", "model": DetailResponseBody}
}

NOT_FOUND_RESPONSE = {
    404: {"description": "Error: Conflict", "model": DetailResponseBody}
}
