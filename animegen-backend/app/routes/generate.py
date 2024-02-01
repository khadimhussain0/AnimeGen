from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.prompt import InputPrompt
from app.models.prompt import Prompt
from app.core.auth import get_current_user
from app.services.model_loader import Model
from io import BytesIO
from PIL import Image

router = APIRouter(
    prefix="/generate",
    tags=["Generate Animes"],
)

@router.post("/")
def generate(
    prompt_data: InputPrompt,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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

    try:
        model = Model()
        images = model.predict(
            prompt=prompt_data.prompt,
            negative_prompt=prompt_data.negative_prompt,
            width=prompt_data.width,
            height=prompt_data.height,
            guidance_scale=prompt_data.guidance_scale,
            num_inference_steps=prompt_data.num_inference_steps
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model could not process the request: {e}")

    # Create a BytesIO buffer to store the streamed image data
    image_stream = BytesIO()

    # Save each image in the list to the BytesIO buffer
    for img in images:
        img.save(image_stream, format="PNG")

    # Reset the buffer position to the beginning
    image_stream.seek(0)

    # Return the processed images as a streaming response
    return StreamingResponse(image_stream, media_type="image/png")
