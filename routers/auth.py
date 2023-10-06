from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.database import db_dependency
from schemas.auth import Token
from services.auth import create_user_access_token, authenticate_user

router = APIRouter(prefix="/login", tags=["login"], )


@router.post("/user", response_model=Token)
async def login_user_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    token = create_user_access_token(user.phone_number, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
