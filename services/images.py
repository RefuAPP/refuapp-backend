import uuid

from fastapi import UploadFile


def save_png_image(image: UploadFile) -> str:
    return _save_image_by_extension(image, ".png")


def save_jpeg_image(image: UploadFile) -> str:
    return _save_image_by_extension(image, ".jpeg")


def _save_image_by_extension(image: UploadFile, extension: str) -> str:
    image_name = f"{uuid.uuid4()}{extension}"
    image_path = f"static/images/refuges/{image_name}"
    with open(image_path, "wb") as buffer:
        buffer.write(image.file.read())
    return image_name
