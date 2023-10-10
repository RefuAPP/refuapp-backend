from pydantic import BaseModel, field_validator, Field

import validators.refuges as validators
from configuration.config import Configuration
from configuration.image import DefaultImage


class Coordinates(BaseModel):
    latitude: float = Field(
        ge=-90, le=90, description='Latitude must be between -90 and 90'
    )
    longitude: float = Field(
        ge=-180, le=180, description='Longitude must be between -180 and 180'
    )


class Capacity(BaseModel):
    winter: int = Field(
        ge=0, description='Winter capacity must be a positive integer'
    )
    summer: int = Field(
        ge=0, description='Summer capacity must be a positive integer'
    )


class Refuge(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        description='Name must be between 1 and 100 characters',
        examples=['Refugi de la Restanca', 'Besiberri'],
    )
    region: str = Field(
        min_length=1,
        max_length=100,
        description='Region must be between 1 and 100 characters',
        examples=['Vielha', 'Benasque'],
    )
    image: str = Field(
        min_length=1,
        max_length=100,
        description='Image must be between 1 and 100 characters',
        default=f'{Configuration.get(DefaultImage)}',
    )
    altitude: int = Field(
        gt=0,
        description='Altitude must be a positive integer',
        examples=[2000, 3000],
    )
    coordinates: Coordinates
    capacity: Capacity

    class Config:
        from_attributes = True

    @field_validator('name', check_fields=True)
    def validate_name(cls, name: str):
        return validators.validate_name(name)

    @field_validator('region', check_fields=True)
    def validate_region(cls, region: str):
        return validators.validate_region(region)


class CreateRefugeRequest(Refuge):
    pass


class CreateRefugeResponse(Refuge):
    id: str


class GetRefugeResponse(Refuge):
    id: str


class UpdateRefugeRequest(Refuge):
    pass


class UpdateRefugeResponse(Refuge):
    id: str


class DeleteRefugeResponse(Refuge):
    id: str
