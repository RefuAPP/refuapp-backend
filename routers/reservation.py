from typing import Annotated

from fastapi import APIRouter, HTTPException, Security
from starlette import status

from models.database import db_dependency
from schemas.auth import TokenData
from schemas.reservation import (
    CreateReservationResponse,
    Reservation,
    Date,
    Reservations,
    DeleteReservationResponse,
)
from services.auth import (
    get_user_id_from_token,
    get_supervisor_id_from_token,
    get_token_data,
)
from services.refuges import find_by_id
from services.reservation import (
    save_reservation,
    get_reservations_by_user,
    get_reservations_for_refuge_and_date,
    user_has_reservation_on_date,
    get_current_time,
    get_reservation_from_id,
    get_reservations_by_refuge_and_user,
    remove_reservation,
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
def create_reservation(
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
    "/{reservation_id}",
    status_code=status.HTTP_200_OK,
    response_model=Reservation,
)
def reservation_from_id(
    reservation_id: str,
    token_data: Annotated[
        TokenData, Security(get_token_data, scopes=['user', 'supervisor'])
    ],
    db: db_dependency,
) -> Reservation:
    if (
        reservation := get_reservation_from_id(
            reservation_id=reservation_id, session=db
        )
    ) is None:
        raise HTTPException(status_code=404, detail='Reservation not found')
    if 'user' in token_data.scopes and reservation.user_id != token_data.id:
        raise HTTPException(
            status_code=403,
            detail='You are not allowed to get a reservation of another user',
        )
    if (
        'supervisor' in token_data.scopes
        and get_supervisor_from_id(supervisor_id=token_data.id, db=db) is None
    ):
        raise HTTPException(
            status_code=403, detail='Supervisor is not found in DB'
        )
    return reservation


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
    if supervisor_id is None:
        raise HTTPException(
            status_code=401,
            detail='You are not authenticated as a supervisor',
        )
    if get_supervisor_from_id(supervisor_id=supervisor_id, db=session) is None:
        raise HTTPException(status_code=403, detail='Supervisor is not in DB')
    if find_by_id(refuge_id=refuge_id, db=session) is None:
        raise HTTPException(status_code=404, detail='Refuge not found')
    date = Date(day=day, month=month, year=year)
    return get_reservations_for_refuge_and_date(refuge_id, date, session)


@router.get(
    "/reservations/refuge/:refuge_id/user/:user_id",
    status_code=status.HTTP_200_OK,
    response_model=Reservations,
)
def get_reservations_for_refuge_and_user(
    refuge_id: str,
    user_id: str,
    current_user_id: get_user_id_from_token,
    session: db_dependency,
) -> Reservations:
    if current_user_id is None:
        raise HTTPException(
            status_code=401,
            detail='You are not authenticated as a user',
        )
    if current_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail='You are not allowed to get the reservations of another user',
        )
    if get_user_from_id(user_id=user_id, db=session) is None:
        raise HTTPException(status_code=404, detail='User not found')
    if find_by_id(refuge_id=refuge_id, db=session) is None:
        raise HTTPException(status_code=404, detail='Refuge not found')
    return get_reservations_by_refuge_and_user(
        refuge_id=refuge_id, user_id=user_id, session=session
    )


@router.delete(
    "/reservations/:reservation_id",
    status_code=status.HTTP_200_OK,
    response_model=DeleteReservationResponse,
)
def delete_reservation(
    reservation_id: str,
    current_user_id: get_user_id_from_token,
    session: db_dependency,
) -> DeleteReservationResponse:
    if current_user_id is None:
        raise HTTPException(
            status_code=401,
            detail='You are not authenticated as a user',
        )
    if (
        reservation := get_reservation_from_id(
            reservation_id=reservation_id, session=session
        )
    ) is None:
        raise HTTPException(status_code=404, detail='Reservation not found')
    if current_user_id != reservation.user_id:
        raise HTTPException(
            status_code=403,
            detail='You are not allowed to delete the reservations of another user',
        )
    remove_reservation(reservation_id, session)
    return DeleteReservationResponse(
        id=reservation_id,
        refuge_id=reservation.refuge_id,
        user_id=reservation.user_id,
        night=reservation.night,
    )
