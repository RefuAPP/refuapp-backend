from datetime import timedelta, datetime
from typing import Annotated, Union, Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Users

router = APIRouter(
    prefix="/login",
    tags=["login"],
)

SECRET_KEY = (
    "fnefthANWsJzOeitxbVhcxfmYdKZMGNY4ieclwBuTl7Mvp1qhwSEKjFB7pOX7X7iaAnS67"
)
ALGORITHM = "HS256"

bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/login/user/token")


class CreateUserRequest(BaseModel):
    username: str
    password: str
    phone_number: str
    emergency_number: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request: CreateUserRequest, db: db_dependency
):
    new_user = Users(
        username=create_user_request.username,
        password=bycrypt_context.hash(create_user_request.password),
        phone_number=create_user_request.phone_number,
        emergency_number=create_user_request.emergency_number,
    )

    db.add(new_user)
    db.commit()


@router.post("/user/token", response_model=Token)
async def login_user_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user',
        )
    token = create_user_access_token(
        user.phone_number, user.id, timedelta(minutes=20)
    )

    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(phone_number: str, password: str, db):
    user = db.query(Users).filter(Users.phone_number == phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not bycrypt_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail='Incorrect password')
    return user


def create_user_access_token(
    phone_number: str, user_id: int, expires_delta: timedelta
):
    encode = {'sub': phone_number, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


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
