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
from app.core.config import FILE_STORAGE_PATH, SERVER_URL, CREDITS_PER_IMAGE
from app.services.model_loader import AnimeGen
import torch



router = APIRouter(
    prefix="/generate",
    tags=["Generate Animes"],
)

anime_gen_instance= AnimeGen()

@router.post("/", response_model=GenerateResponse)
def generate(
    prompt_data: InputPrompt,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    global anime_gen_instance
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
    user_credits = db.query(Credits).filter_by(user_id=current_user.id).first()

    if user_credits and user_credits.amount >= CREDITS_PER_IMAGE:
        user_credits.amount -= CREDITS_PER_IMAGE
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Insufficient credits for image generation.")

    try:
        # images will be a list of PIL.Image objects, so it can contain one or more than one image
        images = anime_gen_instance.generate(
            prompt=prompt_data.prompt,
            negative_prompt=prompt_data.negative_prompt,
            width=prompt_data.width,
            height=prompt_data.height,
            guidance_scale=prompt_data.guidance_scale,
            num_inference_steps=prompt_data.num_inference_steps
        )

        torch.cuda.empty_cache()
        
        # Save images in a directory with UUID and extension, and store the information in the Image table
        for i, image in enumerate(images):
            image_uuid = str(uuid.uuid4())
            image_extension = "png"
            separater = "___"
            process_prompt = str(prompt_data.prompt).replace('/', '_').replace('\\', '_')
            image_filename = f"{process_prompt}{separater}{image_uuid}.{image_extension}"
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
                filename=process_prompt,
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

