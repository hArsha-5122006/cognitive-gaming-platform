from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.patient import Patient
from app.models.game_session import GameSession
from app.models.game_result import GameResult
from app.services.performance_service import calculate_cognitive_scores
from app.services.analytics_service import get_patient_analytics

router = APIRouter()

@router.get("/patient/{patient_id}")
def get_patient_performance(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    sessions = db.query(GameSession).filter(GameSession.patient_id == patient_id).all()
    result = []
    for session in sessions:
        session_results = db.query(GameResult).filter(GameResult.session_id == session.id).all()
        session_data = {
            "session_id": session.id,
            "game_id": session.game_id,
            "score": session.score,
            "accuracy": session.accuracy,
            "time_taken_seconds": session.time_taken_seconds,
            "mistakes": session.mistakes,
            "attempts": session.attempts,
            "difficulty_level": session.difficulty_level,
            "status": session.status,
            "created_at": session.created_at,
            "results": [
                {
                    "question": r.question,
                    "correct_answer": r.correct_answer,
                    "user_answer": r.user_answer,
                    "is_correct": r.is_correct,
                    "reaction_time_ms": r.reaction_time_ms,
                }
                for r in session_results
            ]
        }
        result.append(session_data)
    return result

@router.get("/cognitive_score/{patient_id}")
def get_cognitive_score(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    scores = calculate_cognitive_scores(db, patient_id)
    return scores

@router.get("/analytics/{patient_id}")
def get_analytics(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return get_patient_analytics(db, patient_id)
