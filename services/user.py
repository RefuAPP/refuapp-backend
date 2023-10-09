from typing import Optional

from sqlalchemy.orm import Session

from models.users import Users
from schemas.user import CreateUserRequest, CreateUserResponse
from security.security import get_password_hash


def create_user(
    create_user_request: CreateUserRequest, db: Session
) -> CreateUserResponse:
    new_user = Users(
        username=create_user_request.username,
        password=get_password_hash(create_user_request.password),
        phone_number=create_user_request.phone_number,
        emergency_number=create_user_request.emergency_number,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return CreateUserResponse(
        id=new_user.id,
        username=new_user.username,
        phone_number=new_user.phone_number,
        emergency_number=new_user.emergency_number,
    )


def get_user(user: Users) -> CreateUserResponse:
    return CreateUserResponse(
        id=user.id,
        username=user.username,
        phone_number=user.phone_number,
        emergency_number=user.emergency_number,
    )


def get_user_from_id(user_id: str, db: Session) -> Optional[Users]:
    return db.query(Users).filter_by(id=user_id).first()


def get_user_by_phone_number(phone_number: str, db: Session) -> Optional[Users]:
    return db.query(Users).filter_by(phone_number=phone_number).first()
