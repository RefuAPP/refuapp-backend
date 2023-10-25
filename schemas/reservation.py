from pydantic import BaseModel, model_validator, Field
from datetime import datetime
from typing import List


class Date(BaseModel):
    day: int = Field(ge=1, le=31, examples=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    month: int = Field(
        ge=1, le=12, examples=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    )
    year: int = Field(ge=2023, examples=[2023, 2024, 2025, 2026])

    @model_validator(mode="after")
    def correct_date(self) -> 'Date':
        datetime.strptime(
            f"{self.day}/{self.month}/{self.year}", "%d/%m/%Y"
        ).date()
        return self


class Reservation(BaseModel):
    user_id: str
    refuge_id: str
    night: Date


class ReservationWithId(Reservation):
    id: str


Reservations = List[ReservationWithId]


class CreateReservationResponse(ReservationWithId):
    pass


class DeleteReservationResponse(ReservationWithId):
    pass
