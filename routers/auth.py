from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models.database import db_dependency
from schemas.auth import Token
from services.auth import (
    get_token_for_user,
    get_token_for_admin,
    get_token_for_supervisor,
)
from services.user import get_user_with, get_admin_with, get_supervisor_with

router = APIRouter(
    prefix="/login",
    tags=["login"],
)


@router.post("/", response_model=Token)
async def login_user_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    if form_data.scopes is None:
        raise HTTPException(status_code=401, detail="Scopes not found")
    if len(form_data.scopes) != 1:
        raise HTTPException(status_code=401, detail="Scopes not found")
    if 'user' in form_data.scopes:
        user = get_user_with(form_data.username, form_data.password, db)
        return get_token_for_user(user)
    if 'admin' in form_data.scopes:
        admin = get_admin_with(form_data.username, form_data.password, db)
        return get_token_for_admin(admin)
    if 'supervisor' in form_data.scopes:
        supervisor = get_supervisor_with(
            form_data.username, form_data.password, db
        )
        return get_token_for_supervisor(supervisor)
    raise HTTPException(status_code=401, detail="Illegal scope argument")
