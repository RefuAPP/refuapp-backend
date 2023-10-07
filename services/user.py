from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.users import Users
from schemas.user import CreateUserRequest, CreateUserResponse
from services.security import get_password_hash


def create_user(
    create_user_request: CreateUserRequest, db: Session
) -> CreateUserResponse:
    new_user = Users(
        username=create_user_request.username,
        password=get_password_hash(create_user_request.password),
        phone_number=create_user_request.phone_number,
        emergency_number=create_user_request.emergency_number,
    )

    save_user(new_user, db)

    return CreateUserResponse(
        id=new_user.id,
        username=new_user.username,
        phone_number=new_user.phone_number,
        emergency_number=new_user.emergency_number,
    )


def save_user(user: Users, db: Session):
    if db.query(Users).filter_by(phone_number=user.phone_number).first():
        raise HTTPException(
            status_code=409, detail='Phone number already exists'
        )

    db.add(user)
    db.commit()
