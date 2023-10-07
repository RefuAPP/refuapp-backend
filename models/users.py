import uuid

from sqlalchemy import Column, String

from models.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    username = Column(String)
    password = Column(String)
    phone_number = Column(String, unique=True)
    emergency_number = Column(String)
