from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from models.admins import Admins
from models.users import Users
from schemas.auth import TokenData, Token
from security.token import get_token, get_data_for

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="/login/",
    scopes={
        "user": "User operations",
        "admin": "Admin operations",
        "supervisor": "Supervisor operations",
    },
)


def get_token_for_user(user: Users) -> Token:
    token = get_token(
        TokenData(id=user.id, scopes=['user']), timedelta(days=365)
    )
    return Token(access_token=token, token_type="bearer")


def get_token_for_admin(admin: Admins) -> Token:
    token = get_token(
        TokenData(id=admin.id, scopes=['admin']), timedelta(days=365)
    )
    return Token(access_token=token, token_type="bearer")


def get_token_for_supervisor(supervisor: Admins) -> Token:
    token = get_token(
        TokenData(id=supervisor.id, scopes=['supervisor']),
        timedelta(days=365),
    )
    return Token(access_token=token, token_type="bearer")


def get_id_from_token(token: Annotated[str, Depends(oauth2_bearer)]) -> str:
    if (data := get_data_for(token)) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate identity',
        )
    return data.id


def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)]
) -> str | None:
    user_token = get_data_for(token)
    if user_token is None or 'user' not in user_token.scopes:
        return None
    return user_token.id


def get_current_admin(
    token: Annotated[str, Depends(oauth2_bearer)]
) -> str | None:
    admin_token = get_data_for(token)
    if admin_token is None or 'admin' not in admin_token.scopes:
        return None
    return admin_token.id


def get_token_data(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
    if (data := get_data_for(token)) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not logged in',
        )
    return data


def get_current_supervisor(
    token: Annotated[str, Depends(oauth2_bearer)]
) -> str | None:
    supervisor_token = get_data_for(token)
    if supervisor_token is None or 'supervisor' not in supervisor_token.scopes:
        return None
    return supervisor_token.id


get_user_id_from_token = Annotated[
    str | None, Security(get_current_user, scopes=["user"])
]
get_admin_id_from_token = Annotated[
    str | None, Security(get_current_admin, scopes=["admin"])
]
get_supervisor_id_from_token = Annotated[
    str | None, Security(get_current_supervisor, scopes=["supervisor"])
]
