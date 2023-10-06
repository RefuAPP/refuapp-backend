from fastapi import APIRouter
from starlette import status

from models.database import db_dependency
from schemas.user import CreateUserRequest
from services.user import create_user

router = APIRouter(prefix="/users", tags=["users"], )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_route(create_user_request: CreateUserRequest, db: db_dependency):
    create_user(create_user_request, db)
