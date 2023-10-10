import uuid

from sqlalchemy import Column, String, UUID, ForeignKey, Integer

from models.database import Base


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    refuge_id = Column(String, ForeignKey('refuges.id'))
    user_id = Column(String, ForeignKey('users.id'))
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)
