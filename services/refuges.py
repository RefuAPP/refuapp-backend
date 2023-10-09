from typing import Optional

from sqlalchemy.orm import Session

from models.refuges import Refuges
from schemas.refuge import (
    Refuge,
    CreateRefugeRequest,
    Coordinates,
    Capacity,
    CreateRefugeResponse,
)


# TODO: Check for admin rights, only admin can create refuges
# TODO: Check for authentication
def create_refuge(
    create_refuge_request: CreateRefugeRequest, db: Session
) -> CreateRefugeResponse:
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


def find_by_name(name: str, db: Session) -> Optional[Refuge]:
    return db.query(Refuges).filter_by(name=name).first()
