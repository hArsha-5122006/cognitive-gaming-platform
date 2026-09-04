from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.patient import Patient
from app.schemas.game import GameResultSubmit
from app.services.game_service import save_game_result

router = APIRouter()

@router.post("/submit_result", status_code=201)
def submit_game_result(
    data: GameResultSubmit,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Find patient associated with current user
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=400, detail="Patient profile not found")
    session = save_game_result(db, patient.id, data)
    return {"message": "Result saved", "session_id": session.id}