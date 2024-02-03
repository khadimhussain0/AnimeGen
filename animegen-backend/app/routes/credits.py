from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.credits import Credits
from app.schemas.credits import CreditsAddResponse, GetCreditsResponse
from app.core.auth import get_current_user

router = APIRouter(
    prefix="/credits",
    tags=["User Credits"],
)


@router.get("/", response_model=GetCreditsResponse)
def get_user_credits(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        user_credits = db.query(Credits).filter_by(user_id=current_user.id).first()
        return {"credits": user_credits.amount} if user_credits else {"credits": 0}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.post("/add", response_model=dict)
def add_credits(
    amount: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        user_credits = db.query(Credits).filter_by(user_id=current_user.id).first()
        if not user_credits:
            user_credits = Credits(user_id=current_user.id, amount=0)

        user_credits.amount += amount
        db.add(user_credits)
        db.commit()

        return {"message": "Credits added successfully", "credits": user_credits.amount}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
