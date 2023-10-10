import uuid

from sqlalchemy import Column, String

from models.database import Base


class Supervisors(Base):
    __tablename__ = 'supervisors'

    id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    username = Column(String, unique=True)
    password = Column(String)
