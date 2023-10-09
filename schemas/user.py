from pydantic import BaseModel, Field, field_validator

from validators.user import password_is_valid


class User(BaseModel):
    username: str = Field(
        min_length=1,
        max_length=20,
        description='Username must be between 1 and 20 characters',
        examples=['username'],
    )
    phone_number: str = Field(
        pattern='^[0-9]{9}$',
        description='Phone number must be exactly 9 digits',
    )
    emergency_number: str = Field(
        pattern='^[0-9]{9}$',
        description='Phone number must be exactly 9 digits',
    )


class CreateUserRequest(User):
    password: str = Field(
        max_length=100,
        description='At least 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character',
        examples=['Changeme123!'],
    )

    @field_validator('password')
    def validate_password(cls, password: str):
        return password_is_valid(password)


class CreateUserResponse(User):
    id: str = Field(
        pattern='^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$',
        examples=['123e4567-e89b-12d3-a456-426614174000'],
        description='UUID v4',
    )


class GetUserResponse(CreateUserResponse):
    pass


class UpdateUserRequest(CreateUserRequest):
    pass


class UpdateUserResponse(CreateUserResponse):
    pass
