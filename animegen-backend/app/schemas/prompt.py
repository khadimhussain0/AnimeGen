from pydantic import BaseModel


class InputPrompt(BaseModel):
    prompt: str
    negative_prompt: str = "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name"
    width: int = 832
    height: int = 1216
    guidance_scale: int = 7
    num_inference_steps: int = 28

    class Config:
        orm_mode = True
