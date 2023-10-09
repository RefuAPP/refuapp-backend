from fastapi import APIRouter, HTTPException
from starlette import status

from models.database import db_dependency
from schemas.errors import CONFLICT_RESPONSE
from schemas.user import CreateUserRequest, CreateUserResponse
from services.user import create_user, get_user_by_phone_number

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
async def create_user_route(
    create_user_request: CreateUserRequest, db: db_dependency
):
    if (
        get_user_by_phone_number(create_user_request.phone_number, db)
        is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this phone number already exists",
        )
    return create_user(create_user_request, db)
