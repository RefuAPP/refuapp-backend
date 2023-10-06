from database import Base
from sqlalchemy import Column, Integer, String


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    phone_number = Column(String, unique=True)
    emergency_number = Column(String)
