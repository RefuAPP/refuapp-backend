from fastapi import APIRouter, HTTPException
from starlette import status

from models.database import db_dependency
from schemas.errors import CONFLICT_RESPONSE, NOT_FOUND_RESPONSE
from schemas.refuge import (
    CreateRefugeRequest,
    CreateRefugeResponse,
    GetRefugeResponse,
)
from services.refuges import (
    create_refuge,
    find_by_name,
    find_by_id,
    get_refuge,
    get_all,
)

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
def create_refuge_route(
    create_refuge_request: CreateRefugeRequest, db: db_dependency
) -> CreateRefugeResponse:
    if find_by_name(create_refuge_request.name, db) is not None:
        raise HTTPException(
            status_code=409,
            detail=f"Refuge with name {create_refuge_request.name} already exists",
        )
    return create_refuge(create_refuge_request, db)


@router.get(
    "/{refuge_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetRefugeResponse,
    responses={**NOT_FOUND_RESPONSE},
)
def get_refuge_route(refuge_id: str, db: db_dependency) -> GetRefugeResponse:
    refuge = find_by_id(refuge_id, db)
    if not refuge:
        raise HTTPException(
            status_code=404,
            detail=f"Refuge with id {refuge_id} not found in the database",
        )
    return get_refuge(refuge)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[GetRefugeResponse],
)
def get_refuges_route(db: db_dependency) -> list[GetRefugeResponse]:
    return get_all(db)
