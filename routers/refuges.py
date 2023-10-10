from typing import Annotated

from fastapi import APIRouter, HTTPException, Security
from starlette import status

from models.database import db_dependency
from schemas.auth import TokenData
from schemas.errors import (
    CONFLICT_RESPONSE,
    NOT_FOUND_RESPONSE,
    UNAUTHORIZED_RESPONSE,
    FORBIDDEN_RESPONSE,
)
from schemas.refuge import (
    CreateRefugeRequest,
    CreateRefugeResponse,
    GetRefugeResponse,
    UpdateRefugeResponse,
    UpdateRefugeRequest,
    DeleteRefugeResponse,
)
from services.auth import get_token_data
from services.refuges import (
    create_refuge,
    find_by_name,
    find_by_id,
    get_refuge,
    get_all,
    update_refuge,
    delete_refuge,
)
from services.images import image_in_files

router = APIRouter(
    prefix="/refuges",
    tags=["refuges"],
)

get_token_data_for_create_refuge = Annotated[
    TokenData, Security(get_token_data, scopes=["admin"])
]

get_token_data_for_update_refuge = get_token_data_for_create_refuge

get_token_data_for_delete_refuge = get_token_data_for_create_refuge


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateRefugeResponse,
    responses={
        **CONFLICT_RESPONSE,
        **NOT_FOUND_RESPONSE,
        **UNAUTHORIZED_RESPONSE,
        **FORBIDDEN_RESPONSE,
    },
)
def create_refuge_route(
    create_refuge_request: CreateRefugeRequest,
    token_data: get_token_data_for_create_refuge,
    db: db_dependency,
) -> CreateRefugeResponse:
    if 'admin' not in token_data.scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create a refuge",
        )
    if find_by_name(create_refuge_request.name, db) is not None:
        raise HTTPException(
            status_code=409,
            detail=f"Refuge with name {create_refuge_request.name} already exists",
        )
    if not image_in_files(create_refuge_request.image):
        raise HTTPException(
            status_code=404,
            detail=f"Image with name {create_refuge_request.image} not found in the server",
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


@router.put(
    "/{refuge_id}",
    status_code=status.HTTP_200_OK,
    response_model=UpdateRefugeResponse,
    responses={
        **NOT_FOUND_RESPONSE,
        **CONFLICT_RESPONSE,
        **UNAUTHORIZED_RESPONSE,
        **FORBIDDEN_RESPONSE,
    },
)
def update_refuge_route(
    refuge_id: str,
    update_refuge_request: UpdateRefugeRequest,
    token_data: get_token_data_for_update_refuge,
    db: db_dependency,
) -> UpdateRefugeResponse:
    if 'admin' not in token_data.scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update a refuge",
        )
    refuge = find_by_id(refuge_id, db)
    if not refuge:
        raise HTTPException(
            status_code=404,
            detail=f"Refuge with id {refuge_id} not found in the database",
        )
    if not image_in_files(update_refuge_request.image):
        raise HTTPException(
            status_code=404,
            detail=f"Image with name {update_refuge_request.image} not found in the server",
        )

    refuge_by_name = find_by_name(update_refuge_request.name, db)
    if refuge_by_name is not None and refuge_by_name.id != refuge_id:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot change refuge name to {update_refuge_request.name} because it already exists",
        )

    return update_refuge(refuge, update_refuge_request, db)


@router.delete(
    "/{refuge_id}",
    status_code=status.HTTP_200_OK,
    response_model=DeleteRefugeResponse,
    responses={
        **NOT_FOUND_RESPONSE,
        **UNAUTHORIZED_RESPONSE,
        **FORBIDDEN_RESPONSE,
    },
)
def delete_refuge_route(
    refuge_id: str,
    token_data: get_token_data_for_delete_refuge,
    db: db_dependency,
) -> DeleteRefugeResponse:
    if 'admin' not in token_data.scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete a refuge",
        )
    refuge = find_by_id(refuge_id, db)
    if not refuge:
        raise HTTPException(
            status_code=404,
            detail=f"Refuge with id {refuge_id} not found in the database",
        )
    return delete_refuge(refuge, db)
