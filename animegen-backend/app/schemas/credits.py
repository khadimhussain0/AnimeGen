from typing import List
from pydantic import BaseModel


class CreditsAddResponse(BaseModel):
    amount: int

    class Config:
        orm_mode = True


class GetCreditsResponse(BaseModel):
    credits: int

    class Config:
        orm_mode = True
