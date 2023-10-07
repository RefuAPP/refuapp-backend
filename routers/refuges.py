from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from models.database import db_dependency
from schemas.refuges.create_refuge_request import CreateRefugeRequest
from schemas.refuges.create_refuge_response import CreateRefugeResponse
from services.refuges import create_refuge

router = APIRouter(
    prefix="/refuges",
    tags=["refuges"],
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/login/admin")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateRefugeResponse,
)
async def create_refuge_endpoint(
    create_refuge_request: CreateRefugeRequest, db: db_dependency
):
    return await create_refuge(create_refuge_request, db)
