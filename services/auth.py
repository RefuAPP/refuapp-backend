from datetime import timedelta
from typing import Annotated, Dict

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from models.users import Users
from security.security import verify_password
from security.token import get_token, get_user_id_for

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/login/user")


def get_token_for(user: Users) -> Dict[str, str]:
    token = get_token(user, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}


def get_user_with(phone_number: str, password: str, db: Session):
    user = db.query(Users).filter_by(phone_number=phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not verify_password(password, str(user.password)):
        raise HTTPException(status_code=401, detail='Incorrect password')
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> str:
    if (user_id := get_user_id_for(token)) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user',
        )
    return user_id


get_user_id_from_token = Annotated[str, Depends(get_current_user)]
