import uuid

from sqlalchemy import Column, Integer, String, Float

from configuration.config import Configuration
from models.database import Base

from configuration.image import DefaultImage


class Refuges(Base):
    __tablename__ = 'refuges'

    id = Column(
        String, primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String, unique=True)
    image = Column(
        String,
        default=f'static/images/refuges/{Configuration.get(DefaultImage)}',
    )
    region = Column(String)
    altitude = Column(Integer)
    coordinates_latitude = Column(Float)
    coordinates_longitude = Column(Float)
    capacity_winter = Column(Integer)
    capacity_summer = Column(Integer)
