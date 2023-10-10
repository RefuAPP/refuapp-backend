from sqlalchemy.orm import Session

import schemas
from models.reservation import Reservation
from schemas.reservation import CreateReservationResponse


def save_reservation(
    reservation: schemas.reservation.Reservation, db: Session
) -> CreateReservationResponse:
    new_reservation = Reservation(
        refuge_id=reservation.refuge_id,
        user_id=reservation.user_id,
        day=reservation.night.day,
        month=reservation.night.month,
        year=reservation.night.year,
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return CreateReservationResponse(
        id=new_reservation.id,
        user_id=new_reservation.user_id,
        refuge_id=new_reservation.refuge_id,
        night=schemas.reservation.Date(
            day=new_reservation.day,
            month=new_reservation.month,
            year=new_reservation.year,
        ),
    )
