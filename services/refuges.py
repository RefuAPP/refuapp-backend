from typing import Optional

from sqlalchemy.orm import Session

from configuration.config import Configuration
from configuration.image import DefaultImage
from models.refuges import Refuges
from schemas.refuge import (
    CreateRefugeRequest,
    Coordinates,
    Capacity,
    CreateRefugeResponse,
    GetRefugeResponse,
    UpdateRefugeResponse,
    UpdateRefugeRequest,
    DeleteRefugeResponse,
)
from services.images import delete_image


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


def get_refuge(refuge: Refuges) -> GetRefugeResponse:
    return GetRefugeResponse(
        id=refuge.id,
        name=refuge.name,
        image=refuge.image,
        region=refuge.region,
        altitude=refuge.altitude,
        coordinates=Coordinates(
            latitude=refuge.coordinates_latitude,
            longitude=refuge.coordinates_longitude,
        ),
        capacity=Capacity(
            winter=refuge.capacity_winter,
            summer=refuge.capacity_summer,
        ),
    )


def get_all(db: Session) -> list[GetRefugeResponse]:
    return [get_refuge(refuge) for refuge in find_all(db)]


def update_refuge(
    refuge: Refuges, request: UpdateRefugeRequest, db: Session
) -> UpdateRefugeResponse:
    setattr(refuge, 'name', request.name)
    setattr(refuge, 'image', request.image)
    setattr(refuge, 'region', request.region)
    setattr(refuge, 'altitude', request.altitude)
    setattr(refuge, 'coordinates_latitude', request.coordinates.latitude)
    setattr(refuge, 'coordinates_longitude', request.coordinates.longitude)
    setattr(refuge, 'capacity_winter', request.capacity.winter)
    setattr(refuge, 'capacity_summer', request.capacity.summer)

    db.commit()
    db.refresh(refuge)

    return UpdateRefugeResponse(
        id=refuge.id,
        name=refuge.name,
        image=refuge.image,
        region=refuge.region,
        altitude=refuge.altitude,
        coordinates=Coordinates(
            latitude=refuge.coordinates_latitude,
            longitude=refuge.coordinates_longitude,
        ),
        capacity=Capacity(
            winter=refuge.capacity_winter,
            summer=refuge.capacity_summer,
        ),
    )


def delete_refuge(refuge: Refuges, db: Session) -> DeleteRefugeResponse:
    if refuge.image != Configuration.get(DefaultImage):
        delete_image(str(refuge.image))

    db.delete(refuge)
    db.commit()

    return DeleteRefugeResponse(
        id=refuge.id,
        name=refuge.name,
        image=refuge.image,
        region=refuge.region,
        altitude=refuge.altitude,
        coordinates=Coordinates(
            latitude=refuge.coordinates_latitude,
            longitude=refuge.coordinates_longitude,
        ),
        capacity=Capacity(
            winter=refuge.capacity_winter,
            summer=refuge.capacity_summer,
        ),
    )


def find_by_name(name: str, db: Session) -> Optional[Refuges]:
    return db.query(Refuges).filter_by(name=name).first()


def find_by_id(refuge_id: str, db: Session) -> Optional[Refuges]:
    return db.query(Refuges).filter_by(id=refuge_id).first()


def find_all(db: Session) -> list[Refuges]:
    return db.query(Refuges).all()
