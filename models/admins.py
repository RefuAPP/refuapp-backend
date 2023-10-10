import uuid

from sqlalchemy import Column, String

from models.database import Base


class Admins(Base):
    __tablename__ = 'admins'

    id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    username = Column(String, unique=True)
    password = Column(String)
