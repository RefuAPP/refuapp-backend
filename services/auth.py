from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from models.users import Users
from schemas.auth import TokenData, Token
from security.token import get_token, get_data_for

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/login/", scopes={"user": "User operations", "admin": "Admin operations",
                                                                 "supervisor": "Supervisor operations"})


def get_token_for_user(user: Users) -> Token:
    token = get_token(TokenData(id=user.id, scopes=['user']), timedelta(minutes=20))
    return Token(access_token=token, token_type="bearer")


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> str:
    if (user_token := get_data_for(token)) is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user', )
    if 'user' not in user_token.scopes:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Privilege error (can\'t access the '
                                                                             'resource')
    return user_token.id


get_user_id_from_token = Annotated[str, Depends(get_current_user)]
