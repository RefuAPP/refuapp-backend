from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.admins import Admins
from models.users import Users
from schemas.user import (
    CreateUserRequest,
    CreateUserResponse,
    UpdateUserRequest,
    UpdateUserResponse,
    GetUserResponse,
    DeleteUserResponse,
)
from security.security import get_password_hash, verify_password


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


def get_user(user: Users) -> GetUserResponse:
    return GetUserResponse(
        id=user.id,
        username=user.username,
        phone_number=user.phone_number,
        emergency_number=user.emergency_number,
    )


def update_user(
    user: Users, request: UpdateUserRequest, db: Session
) -> UpdateUserResponse:
    setattr(user, 'username', request.username)
    setattr(user, 'phone_number', request.phone_number)
    setattr(user, 'emergency_number', request.emergency_number)
    setattr(user, 'password', get_password_hash(request.password))

    db.commit()
    db.refresh(user)

    return UpdateUserResponse(
        id=user.id,
        username=user.username,
        phone_number=user.phone_number,
        emergency_number=user.emergency_number,
    )


def delete_user(user: Users, db: Session) -> DeleteUserResponse:
    db.delete(user)
    db.commit()

    return DeleteUserResponse(
        id=user.id,
        username=user.username,
        phone_number=user.phone_number,
        emergency_number=user.emergency_number,
    )


def get_user_from_id(user_id: str, db: Session) -> Optional[Users]:
    return db.query(Users).filter_by(id=user_id).first()


def get_admin_from_id(admin_id: str, db: Session) -> Optional[Admins]:
    return db.query(Admins).filter_by(id=admin_id).first()


def get_user_by_phone_number(phone_number: str, db: Session) -> Optional[Users]:
    return db.query(Users).filter_by(phone_number=phone_number).first()


def get_user_with(phone_number: str, password: str, db: Session):
    user = db.query(Users).filter_by(phone_number=phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not verify_password(password, str(user.password)):
        raise HTTPException(status_code=401, detail='Incorrect password')
    return user


def get_admin_with(username: str, password: str, db: Session):
    admin = db.query(Admins).filter_by(username=username).first()
    if not admin:
        raise HTTPException(status_code=404, detail='Admin not found')
    if not verify_password(password, str(admin.password)):
        raise HTTPException(status_code=401, detail='Incorrect password')
    return admin
