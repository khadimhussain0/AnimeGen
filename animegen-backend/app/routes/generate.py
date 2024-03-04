import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.prompt import InputPrompt
from app.schemas.image import ImageResponse, GenerateResponse
from app.models.prompt import Prompt
from app.models.image import Image
from app.models.credits import Credits
from app.core.auth import get_current_user
from app.core.config import FILE_STORAGE_PATH, SERVER_URL
from app.services.model_loader import Model


router = APIRouter(
    prefix="/generate",
    tags=["Generate Animes"],
)


@router.post("/", response_model=GenerateResponse)
def generate(
    prompt_data: InputPrompt,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Saving prompt data in the Prompt table
    prompt = Prompt(
        user_id=current_user.id,
        prompt=prompt_data.prompt,
        negative_prompt=prompt_data.negative_prompt,
        width=prompt_data.width,
        height=prompt_data.height,
        guidance_scale=prompt_data.guidance_scale,
        num_inference_steps=prompt_data.num_inference_steps,
    )
    db.add(prompt)
    db.commit()
    db.refresh(prompt)

    images_info = []

    # Deduct credits after a successful generation
    credits_to_deduct = 3
    user_credits = db.query(Credits).filter_by(user_id=current_user.id).first()

    if user_credits and user_credits.amount >= credits_to_deduct:
        user_credits.amount -= credits_to_deduct
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Insufficient credits for image generation.")

    try:
        model = Model()
        # images will be a list of PIL.Image objects, so it can contain one or more than one image
        images = model.predict(
            prompt=prompt_data.prompt,
            negative_prompt=prompt_data.negative_prompt,
            width=prompt_data.width,
            height=prompt_data.height,
            guidance_scale=prompt_data.guidance_scale,
            num_inference_steps=prompt_data.num_inference_steps
        )
        
        # Save images in a directory with UUID and extension, and store the information in the Image table
        for i, image in enumerate(images):
            image_uuid = str(uuid.uuid4())
            image_extension = "png"
            separater = "___"
            image_filename = f"{prompt_data.prompt}{separater}{image_uuid}.{image_extension}"
            url = f"{SERVER_URL}/images/api/v1/{image_filename}"
            image_path = f"{FILE_STORAGE_PATH}/{image_filename}"
            image.save(image_path)

            # Saving image information in the Image table
            db_image = Image(
                user_id=current_user.id,
                prompt_id=prompt.id,
                uuid=image_uuid,
                width=image.width,
                height=image.height,
                extension=image_extension,
                filename=prompt_data.prompt,
                separater=separater
            )
            db.add(db_image)
            db.commit()
            db.refresh(db_image)

            image_id = db_image.id

            # Append image information to the list for the response
            images_info.append(ImageResponse(
                filename=image_filename,
                url=url,
                key=image_id,
            ))

        db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model could not process the request: {e}")

    return GenerateResponse(message="Images generated and saved successfully.", images=images_info)

