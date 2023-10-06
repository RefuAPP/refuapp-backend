from sqlalchemy.orm import Session

from models.users import Users
from schemas.user import CreateUserRequest
from services.security import get_password_hash


def create_user(create_user_request: CreateUserRequest, db: Session):
    new_user = Users(username=create_user_request.username,
                     password=get_password_hash(create_user_request.password),
                     phone_number=create_user_request.phone_number,
                     emergency_number=create_user_request.emergency_number, )
    db.add(new_user)
    db.commit()
