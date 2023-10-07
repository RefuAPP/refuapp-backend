from sqlalchemy import Column, Integer, String, Float

from models.database import Base


class Refuges(Base):
    __tablename__ = 'refuges'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    image = Column(String)  # TODO: Put default image
    region = Column(String)
    altitude = Column(Integer)
    coordinates_latitude = Column(Float)
    coordinates_longitude = Column(Float)
    capacity_winter = Column(Integer)
    capacity_summer = Column(Integer)