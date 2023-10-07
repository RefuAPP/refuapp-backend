from datetime import timedelta, datetime
from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from models.users import Users
from services.security import verify_password

SECRET_KEY = (
    "fnefthANWsJzOeitxbVhcxfmYdKZMGNY4ieclwBuTl7Mvp1qhwSEKjFB7pOX7X7iaAnS67"
)
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/login/user")


def create_user_access_token(
    phone_number: str, user_id: int, expires_delta: timedelta
):
    encode = {'sub': phone_number, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(phone_number: str, password: str, db: Session):
    user = db.query(Users).filter_by(phone_number=phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not verify_password(password, str(user.password)):
        raise HTTPException(status_code=401, detail='Incorrect password')
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone_number: Optional[str] = payload.get('sub')
        user_id: Optional[int] = payload.get('id')
        if phone_number is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate user',
            )
        return {'phone_number': phone_number, 'id': user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user',
        )


user_logged_in_dependency = Annotated[dict, Depends(get_current_user)]
