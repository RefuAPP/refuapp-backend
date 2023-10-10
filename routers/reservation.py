from fastapi import APIRouter, HTTPException
from starlette import status

from models.database import db_dependency
from schemas.reservation import CreateReservationResponse, Reservation
from services.auth import get_user_id_from_token
from services.refuges import find_by_id
from services.reservation import save_reservation
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
    if user_id != reservation.user_id:  # type: ignore
        raise HTTPException(
            status_code=403,
            detail='You are not allowed to create a reservation',
        )
    if find_by_id(refuge_id=reservation.refuge_id, db=session) is None:
        raise HTTPException(status_code=404, detail='Refuge not found')
    if get_user_from_id(user_id=reservation.user_id, db=session) is None:
        raise HTTPException(status_code=404, detail='User not found')
    return save_reservation(reservation, session)
