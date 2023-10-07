from sqlalchemy.orm import Session
from models.refuges import Refuges
from schemas.refuges.capacity import Capacity
from schemas.refuges.coordinates import Coordinates
from schemas.refuges.create_refuge_request import CreateRefugeRequest
from schemas.refuges.create_refuge_response import CreateRefugeResponse


async def create_refuge(
    create_refuge_request: CreateRefugeRequest, db: Session
):
    new_refuge = Refuges(
        name=create_refuge_request.name,
        image=create_refuge_request.image,
        region=create_refuge_request.region,
        altitude=create_refuge_request.altitude,
        coordinates_latitude=create_refuge_request.coordinates.latitude,
        coordinates_longitude=create_refuge_request.coordinates.longitude,
        capacity_winter=create_refuge_request.capacity.winter,
        capacity_summer=create_refuge_request.capacity.summer,
    )

    db.add(new_refuge)
    db.commit()
    db.refresh(new_refuge)

    return CreateRefugeResponse(
        id=new_refuge.id,
        name=new_refuge.name,
        image=new_refuge.image,
        region=new_refuge.region,
        altitude=new_refuge.altitude,
        coordinates=Coordinates(
            latitude=new_refuge.coordinates_latitude,
            longitude=new_refuge.coordinates_longitude,
        ),
        capacity=Capacity(
            winter=new_refuge.capacity_winter,
            summer=new_refuge.capacity_summer,
        ),
    )
