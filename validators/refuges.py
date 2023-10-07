from fastapi import HTTPException

from schemas.refuges.capacity import Capacity
from schemas.refuges.coordinates import Coordinates


def validate_coordinates(coordinates: Coordinates) -> Coordinates:
    if not float(coordinates.latitude) or not float(coordinates.longitude):
        raise HTTPException(status_code=400, detail='Invalid coordinates')
    if coordinates.latitude < -90 or coordinates.latitude > 90:
        raise HTTPException(
            status_code=400, detail='Latitude must be between -90 and 90'
        )
    if coordinates.longitude < -180 or coordinates.longitude > 180:
        raise HTTPException(
            status_code=400, detail='Longitude must be between -180 and 180'
        )
    return coordinates


def validate_name(name: str) -> str:
    if not name:
        raise HTTPException(
            status_code=400, detail='Name must be a non-empty string'
        )
    if len(name) > 100:
        raise HTTPException(
            status_code=400, detail='Name must be less than 100 characters'
        )
    if not name.strip(' ')[0].istitle():
        raise HTTPException(
            status_code=400, detail='Name must start with a capital letter'
        )
    return name


def validate_image(image: str) -> str:
    if not image:
        raise HTTPException(
            status_code=400, detail='Image must be a non-empty string'
        )
    if len(image) > 100:
        raise HTTPException(
            status_code=400, detail='Image must be less than 100 characters'
        )
    return image


def validate_region(region: str) -> str:
    if not region:
        raise HTTPException(
            status_code=400, detail='Region must be a non-empty string'
        )
    if len(region) > 100:
        raise HTTPException(
            status_code=400, detail='Region must be less than 100 characters'
        )
    if not region.istitle():
        raise HTTPException(
            status_code=400, detail='Region must be capitalized'
        )
    return region


def validate_altitude(altitude: int) -> int:
    if not altitude:
        raise HTTPException(
            status_code=400, detail='Altitude must be a non-empty integer'
        )
    if altitude < 0:
        raise HTTPException(
            status_code=400, detail='Altitude must be a positive integer'
        )
    return altitude


def validate_capacity(capacity: Capacity) -> Capacity:
    if not capacity:
        raise HTTPException(
            status_code=400, detail='Capacity must be a non-empty integer'
        )
    if capacity.winter < 0:
        raise HTTPException(
            status_code=400, detail='Winter capacity must be a positive integer'
        )
    if capacity.summer < 0:
        raise HTTPException(
            status_code=400, detail='Summer capacity must be a positive integer'
        )
    return capacity
