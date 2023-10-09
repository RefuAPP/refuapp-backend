from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.database import db_dependency
from schemas.auth import Token
from services.auth import get_token_for, get_user_with

router = APIRouter(
    prefix="/login",
    tags=["login"],
)


@router.post("/user", response_model=Token)
async def login_user_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user = get_user_with(form_data.username, form_data.password, db)
    return get_token_for(user)
