from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from models.database import get_db
from schemas.auth import Token
from schemas.user import CreateUserRequest
from services.auth import create_user_access_token, authenticate_user
from services.user import create_user

router = APIRouter(prefix="/login", tags=["login"], )

db_dependency = Annotated[Session, Depends(get_db)]


# TODO: this go to routes/user.py
@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user_route(create_user_request: CreateUserRequest, db: db_dependency):
    create_user(create_user_request, db)


@router.post("/user/token", response_model=Token)
async def login_user_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    token = create_user_access_token(user.phone_number, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
