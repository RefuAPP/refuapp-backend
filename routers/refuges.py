from fastapi import APIRouter
from starlette import status

from models.database import db_dependency
from schemas.refuge import CreateRefugeRequest, Refuge
from services.refuges import create_refuge

router = APIRouter(
    prefix="/refuges",
    tags=["refuges"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Refuge,
)
def create_refuge_endpoint(
    create_refuge_request: CreateRefugeRequest, db: db_dependency
):
    return create_refuge(create_refuge_request, db)
