from fastapi import APIRouter, HTTPException
from starlette import status

from models.database import db_dependency
from schemas.refuge import CreateRefugeRequest, Refuge, CreateRefugeResponse
from services.refuges import create_refuge, find_by_name

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
) -> CreateRefugeResponse:
    if not find_by_name(create_refuge_request.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Refuge with name {create_refuge_request.name} already exists",
        )
    return create_refuge(create_refuge_request, db)
