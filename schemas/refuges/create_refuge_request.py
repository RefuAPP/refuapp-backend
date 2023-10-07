from pydantic import BaseModel, field_validator

import validators.refuges
from schemas.refuges.capacity import Capacity
from schemas.refuges.coordinates import Coordinates


class CreateRefugeRequest(BaseModel):
    coordinates: Coordinates
    name: str
    image: str
    region: str
    altitude: int
    capacity: Capacity

    class Config:
        from_attributes = True

    @field_validator('coordinates', check_fields=True)
    def validate_positive(cls, coordinates: Coordinates):
        return validators.refuges.validate_coordinates(coordinates)

    @field_validator('name', check_fields=True)
    def validate_name(cls, name: str):
        return validators.refuges.validate_name(name)

    @field_validator('image', check_fields=True)
    def validate_image(cls, image: str):
        return validators.refuges.validate_image(image)

    @field_validator('region', check_fields=True)
    def validate_region(cls, region: str):
        return validators.refuges.validate_region(region)

    @field_validator('altitude', check_fields=True)
    def validate_altitude(cls, altitude: int):
        return validators.refuges.validate_altitude(altitude)

    @field_validator('capacity', check_fields=True)
    def validate_capacity(cls, capacity: Capacity):
        return validators.refuges.validate_capacity(capacity)
