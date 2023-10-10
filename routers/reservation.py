from fastapi import APIRouter, HTTPException
from starlette import status

from models.database import db_dependency
from schemas.reservation import (
    CreateReservationResponse,
    Reservation,
    Date,
    Reservations,
)
from services.auth import get_user_id_from_token
from services.refuges import find_by_id
from services.reservation import (
    save_reservation,
    get_reservations_by_user,
    get_reservations_for_refuge_and_date,
)
from services.user import get_user_from_id

router = APIRouter(
    prefix="/reservations",
    tags=["reservation"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateReservationResponse,
)
def create_reservation_route(
    reservation: Reservation,
    user_id=get_user_id_from_token,
    session=db_dependency,
):
    if user_id != reservation.user_id:
        raise HTTPException(
            status_code=403,
            detail='You are not allowed to create a reservation',
        )
    if find_by_id(refuge_id=reservation.refuge_id, db=session) is None:
        raise HTTPException(status_code=404, detail='Refuge not found')
    if get_user_from_id(user_id=reservation.user_id, db=session) is None:
        raise HTTPException(status_code=404, detail='User not found')
    return save_reservation(reservation, session)


@router.get(
    "/user/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=Reservations,
)
def get_reservations_for_user(
    user_id: str, logged_user_id: get_user_id_from_token, db: db_dependency
) -> Reservations:
    if user_id != logged_user_id:
        raise HTTPException(
            status_code=403,
            detail='You are not allowed to get the reservations of another user',
        )
    if get_user_from_id(user_id=user_id, db=db) is None:
        raise HTTPException(status_code=404, detail='User not found')
    return get_reservations_by_user(user_id, db)


@router.get(
    "/refuge/{refuge_id}/year/{year}/month/{month}/day/{day}/",
    status_code=status.HTTP_200_OK,
    response_model=Reservations,
)
def get_reservations_for_refuge_in_date(
    refuge_id: str,
    year: int,
    month: int,
    day: int,
    session=db_dependency,
) -> Reservations:
    if find_by_id(refuge_id=refuge_id, db=session) is None:
        raise HTTPException(status_code=404, detail='Refuge not found')
    date = Date(day=day, month=month, year=year)
    return get_reservations_for_refuge_and_date(refuge_id, date, session)
