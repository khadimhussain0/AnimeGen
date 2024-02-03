from typing import List
from pydantic import BaseModel


class ImageResponse(BaseModel):
    filename: str
    url: str
    key: int

    class Config:
        orm_mode = True


class GenerateResponse(BaseModel):
    message: str
    images: List[ImageResponse]

    class Config:
        orm_mode = True
