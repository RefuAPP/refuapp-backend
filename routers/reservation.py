from datetime import datetime

import ntplib
from fastapi import APIRouter, HTTPException
from starlette import status

from models.database import db_dependency
from schemas.reservation import (
    CreateReservationResponse,
    Reservation,
    Date,
    Reservations,
)
from services.auth import get_user_id_from_token, get_supervisor_id_from_token
from services.refuges import find_by_id
from services.reservation import (
    save_reservation,
    get_reservations_by_user,
    get_reservations_for_refuge_and_date,
    user_has_reservation_on_date,
    get_current_time,
)
from services.user import get_user_from_id, get_supervisor_from_id

router = APIRouter(
    prefix="/reservations",
    tags=["reservation"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateReservationResponse,
)
def reservation_for_user(
    reservation: Reservation,
    user_id: get_user_id_from_token,
    session: db_dependency,
) -> CreateReservationResponse:
    if user_id != reservation.user_id:
        raise HTTPException(
            status_code=403,
            detail='You are not allowed to create a reservation',
        )
    if find_by_id(refuge_id=reservation.refuge_id, db=session) is None:
        raise HTTPException(status_code=404, detail='Refuge not found')
    if get_user_from_id(user_id=reservation.user_id, db=session) is None:
        raise HTTPException(status_code=404, detail='User not found')
    if user_has_reservation_on_date(
        user_id=reservation.user_id, night=reservation.night, session=session
    ):
        raise HTTPException(
            status_code=403,
            detail='User already has a reservation on this date',
        )
    if (current_time := get_current_time()) is None:
        raise HTTPException(
            status_code=500,
            detail='Error getting current time from ntp server, try again',
        )
    if (
        reservation.night.year < current_time.year
        or reservation.night.month < current_time.month
        or reservation.night.day < current_time.day
    ):
        raise HTTPException(
            status_code=403,
            detail='You cannot make a reservation for a past date',
        )
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
    supervisor_id: get_supervisor_id_from_token,
    session: db_dependency,
) -> Reservations:
    if find_by_id(refuge_id=refuge_id, db=session) is None:
        raise HTTPException(status_code=404, detail='Refuge not found')
    if get_supervisor_from_id(supervisor_id=supervisor_id, db=session) is None:
        raise HTTPException(status_code=404, detail='Supervisor not found')
    date = Date(day=day, month=month, year=year)
    return get_reservations_for_refuge_and_date(refuge_id, date, session)