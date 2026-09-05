from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.adaptive_service import recommend_difficulty

router = APIRouter()

@router.get("/difficulty/{patient_id}/{game_id}")
def get_recommended_difficulty(
    patient_id: int,
    game_id: int,
    db: Session = Depends(get_db)
):
    return recommend_difficulty(db, patient_id, game_id)