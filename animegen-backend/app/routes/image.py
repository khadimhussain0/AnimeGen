import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.image import Image
from app.core.auth import get_current_user
from fastapi.responses import StreamingResponse
from app.schemas.image import GenerateResponse
from app.core.config import FILE_STORAGE_PATH, SERVER_URL

router = APIRouter(
    prefix="/images",
    tags=["Image Service"],
)


@router.get("/", response_model=GenerateResponse)
def get_user_images(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        user_images = db.query(Image).filter_by(user_id=current_user.id).all()

        images_info = []
        for i, image in enumerate(user_images):
            filename = f"{image.filename}{image.separater}{image.uuid}.{image.extension}"
            url = f"{SERVER_URL}/images/api/v1/{filename}"
            images_info.append({"filename": filename, "url": url, "key": image.id})

        return GenerateResponse(message="Fetched all images.", images=images_info)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.get("/community", response_model=GenerateResponse)
def get_community_images(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        user_images = db.query(Image).filter_by(is_community=True).all()
        images_info = []
        for i, image in enumerate(user_images):
            filename = f"{image.filename}{image.separater}{image.uuid}.{image.extension}"
            url = f"{SERVER_URL}/images/api/v1/{filename}"
            images_info.append({"filename": filename, "url": url, "key": image.id})

        return GenerateResponse(message="Fetched all images.", images=images_info)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.get("/api/v1/{filename}")
def serve_image(filename: str):
    try:
        image_path = f"{FILE_STORAGE_PATH}/{filename}"

        if os.path.exists(image_path):
            return StreamingResponse(open(image_path, "rb"), media_type="image/png")
        else:
            raise HTTPException(status_code=404, detail="Image not found.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
