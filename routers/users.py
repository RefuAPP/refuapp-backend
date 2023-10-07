from fastapi import APIRouter
from starlette import status

from models.database import db_dependency
from schemas.user import CreateUserRequest, CreateUserResponse
from services.user import create_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse
)
async def create_user_route(
    create_user_request: CreateUserRequest, db: db_dependency
):
    return create_user(create_user_request, db)
