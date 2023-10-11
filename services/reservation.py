from datetime import datetime

import ntplib  # type: ignore
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
                .filter(Reservation.refuge_id == refuge_id)
                .filter(Reservation.day == date.day)
                .filter(Reservation.month == date.month)
                .filter(Reservation.year == date.year)
                .all()
            ),
        )
    )


def user_has_reservation_on_date(
    user_id: str, night: Date, session: Session
) -> bool:
    return (
        session.query(Reservation)
        .filter(Reservation.user_id == user_id)
        .filter(Reservation.day == night.day)
        .filter(Reservation.month == night.month)
        .filter(Reservation.year == night.year)
        .first()
        is not None
    )


def get_current_time() -> datetime | None:
    try:
        ntp_client = ntplib.NTPClient()
        unix_time_es = ntp_client.request('es.pool.ntp.org').tx_time
        return datetime.fromtimestamp(unix_time_es)
    except ntplib.NTPException:
        return None