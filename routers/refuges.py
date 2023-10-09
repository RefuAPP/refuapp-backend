from fastapi import APIRouter, HTTPException
from starlette import status

from models.database import db_dependency
from schemas.errors import CONFLICT_RESPONSE
from schemas.refuge import CreateRefugeRequest, CreateRefugeResponse
from services.refuges import create_refuge, find_by_name

router = APIRouter(
    prefix="/refuges",
    tags=["refuges"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateRefugeResponse,
    responses={**CONFLICT_RESPONSE},
)
def create_refuge_endpoint(
    create_refuge_request: CreateRefugeRequest, db: db_dependency
) -> CreateRefugeResponse:
    if find_by_name(create_refuge_request.name, db) is not None:
        raise HTTPException(
            status_code=409,
            detail=f"Refuge with name {create_refuge_request.name} already exists",
        )
    return create_refuge(create_refuge_request, db)
