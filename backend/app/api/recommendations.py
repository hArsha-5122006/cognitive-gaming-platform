from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.auth import get_current_user
from app.core.permissions import get_patient_if_authorized
from app.services.adaptive_service import recommend_difficulty
from app.services.recommendation_service import recommend_next_game
from app.services.training_plan_service import generate_training_plan

router = APIRouter()

@router.get("/difficulty/{patient_id}/{game_id}")
def get_recommended_difficulty(
    patient_id: int,
    game_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    get_patient_if_authorized(patient_id, current_user, db)
    return recommend_difficulty(db, patient_id, game_id)

@router.get("/next_game/{patient_id}")
def get_next_game_recommendation(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    get_patient_if_authorized(patient_id, current_user, db)
    return recommend_next_game(db, patient_id)

@router.get("/training_plan/{patient_id}")
def get_training_plan(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    get_patient_if_authorized(patient_id, current_user, db)
    return generate_training_plan(db, patient_id)
