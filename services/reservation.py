from sqlalchemy.orm import Session

import schemas
from models.reservation import Reservation
from schemas.reservation import (
    CreateReservationResponse,
    Reservations,
    Date,
)


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


def get_reservations_by_user(user_id: str, session: Session) -> Reservations:
    return list(
        map(
            lambda res: str(res.id),
            (
                session.query(Reservation)
                .filter(Reservation.user_id == user_id)
                .all()
            ),
        )
    )


def get_reservations_for_refuge_and_date(
    refuge_id: str, date: Date, session: Session
) -> Reservations:
    return list(
        map(
            lambda res: str(res.id),
            (
                session.query(Reservation)
                .filter(
                    Reservation.refuge_id == refuge_id
                    and Reservation.day == date.day
                    and Reservation.month == date.month
                    and Reservation.year == date.year
                )
                .all()
            ),
        )
    )
