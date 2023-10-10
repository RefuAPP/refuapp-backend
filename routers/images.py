from fastapi import APIRouter, UploadFile, HTTPException
from starlette import status

from schemas.errors import INVALID_REQUEST

from services.images import save_jpeg_image, save_png_image

router = APIRouter(
    prefix="/images",
    tags=["images"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=str,
    responses={**INVALID_REQUEST},
)
def create_image_route(image: UploadFile) -> str:
    if image.content_type != "image/jpeg" and image.content_type != "image/png":
        raise HTTPException(
            status_code=400, detail="Image must be a JPEG or PNG file"
        )
    if image.content_type == "image/jpeg":
        return save_jpeg_image(image)
    else:
        return save_png_image(image)
