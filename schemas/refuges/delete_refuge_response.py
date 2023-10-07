from pydantic import BaseModel

from schemas.refuges.capacity import Capacity
from schemas.refuges.coordinates import Coordinates


class UpdateRefugeRequest(BaseModel):
    id: int
    coordinates: Coordinates
    name: str
    image: str
    region: str
    altitude: int
    capacity: Capacity
