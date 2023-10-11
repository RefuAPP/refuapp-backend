from typing import Optional, Annotated

from fastapi import APIRouter, HTTPException, Security
from starlette import status

from models.database import db_dependency
from models.users import Users
from schemas.auth import TokenData
from schemas.errors import (
    CONFLICT_RESPONSE,
    NOT_FOUND_RESPONSE,
    UNAUTHORIZED_RESPONSE,
    FORBIDDEN_RESPONSE,
)
from schemas.user import (
    CreateUserRequest,
    CreateUserResponse,
    GetUserResponse,
    UpdateUserResponse,
    UpdateUserRequest,
    DeleteUserResponse,
)
from services.auth import (
    get_user_id_from_token,
    get_token_data,
)
from services.user import (
    create_user,
    get_user_by_phone_number,
    get_user_from_id,
    get_user,
    update_user,
    delete_user,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserResponse,
    responses={**CONFLICT_RESPONSE},
)
def create_user_route(
    create_user_request: CreateUserRequest, db: db_dependency
) -> CreateUserResponse:
    if (
        get_user_by_phone_number(create_user_request.phone_number, db)
        is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this phone number already exists",
        )

    return create_user(create_user_request, db)


get_token_data_for_get_user = Annotated[
    TokenData, Security(get_token_data, scopes=["user", "supervisor"])
]


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetUserResponse,
    responses={
        **NOT_FOUND_RESPONSE,
        **UNAUTHORIZED_RESPONSE,
        **FORBIDDEN_RESPONSE,
    },
)
def get_user_route(
    user_id: str, token_data: get_token_data_for_get_user, db: db_dependency
) -> GetUserResponse:
    if token_data.id != user_id and 'supervisor' not in token_data.scopes:
        raise HTTPException(
            status_code=403,
            detail='You are not allowed to access this resource',
        )

    user: Optional[Users] = get_user_from_id(user_id, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this id does not exist",
        )
    return get_user(user)


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UpdateUserResponse,
    responses={
        **NOT_FOUND_RESPONSE,
        **UNAUTHORIZED_RESPONSE,
        **CONFLICT_RESPONSE,
        **FORBIDDEN_RESPONSE,
    },
)
def update_user_route(
    user_id: str,
    update_user_request: UpdateUserRequest,
    logged_user_id: get_user_id_from_token,
    db: db_dependency,
):
    check_target_user_is_logged_user(user_id, logged_user_id)
    user: Optional[Users] = get_user_from_id(user_id, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this id does not exist",
        )

    if (
        user.phone_number != update_user_request.phone_number
        and get_user_by_phone_number(update_user_request.phone_number, db)
        is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this phone number already exists",
        )
    return update_user(user, update_user_request, db)


def check_target_user_is_logged_user(user_id: str, logged_user_id: str | None):
    if logged_user_id is None:
        raise HTTPException(status_code=401, detail='You are not logged in')
    if logged_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail='You are not allowed to access this resource',
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=DeleteUserResponse,
    responses={
        **NOT_FOUND_RESPONSE,
        **UNAUTHORIZED_RESPONSE,
        **FORBIDDEN_RESPONSE,
    },
)
def delete_user_route(
    user_id: str, logged_user_id: get_user_id_from_token, db: db_dependency
) -> DeleteUserResponse:
    check_target_user_is_logged_user(user_id, logged_user_id)
    user: Optional[Users] = get_user_from_id(user_id, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this id does not exist",
        )
    return delete_user(user, db)
