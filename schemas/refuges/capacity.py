from pydantic import BaseModel


class Capacity(BaseModel):
    winter: int
    summer: int
