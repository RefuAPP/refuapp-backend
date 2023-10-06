from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    password: str
    phone_number: str
    emergency_number: str

    class Config:
        orm_mode = True

