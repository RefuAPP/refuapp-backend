from fastapi import APIRouter, status
from fastapi.responses import FileResponse

from schemas.errors import NOT_FOUND_RESPONSE
from services.csv import CSV_DATA_DIR

router = APIRouter(
    prefix="/data",
    tags=["data"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
    responses={**NOT_FOUND_RESPONSE},
)
def get_csv_file(file_name: str):
    return FileResponse(f"{CSV_DATA_DIR}{file_name}")
