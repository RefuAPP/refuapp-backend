from pydantic import BaseModel, field_validator

from validators.user import (
    phone_number_is_exactly_9_digits,
    username_is_not_empty,
    password_is_valid,
)


class CreateUserRequest(BaseModel):
    username: str
    password: str
    phone_number: str
    emergency_number: str

    class Config:
        from_atributes = True

    @field_validator('phone_number')
    def phone_number_is_exactly_9_digits(cls, v):
        return phone_number_is_exactly_9_digits(v)

    @field_validator('emergency_number')
    def emergency_number_is_exactly_9_digits(cls, v):
        return phone_number_is_exactly_9_digits(v)

    @field_validator('username')
    def username_is_not_empty(cls, v):
        return username_is_not_empty(v)

    @field_validator('password')
    def password_is_valid(cls, v):
        return password_is_valid(v)


class CreateUserResponse(BaseModel):
    id: str
    username: str
    phone_number: str
    emergency_number: str
