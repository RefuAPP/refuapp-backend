from pydantic import BaseModel

from schemas.refuges.capacity import Capacity
from schemas.refuges.coordinates import Coordinates


class UpdateRefugeResponse(BaseModel):
    id: int
    coordinates: Coordinates
    name: str
    image: str
    region: str
    altitude: int
    capacity: Capacity
