from sqlalchemy.orm import Session
from collections import defaultdict
from app.models.caregiver import Caregiver
from app.models.patient import Patient
from app.models.game_session import GameSession
from app.models.game import Game

def get_caregiver_patients(db: Session, caregiver_user_id: int):
    caregiver = db.query(Caregiver).filter(Caregiver.user_id == caregiver_user_id).first()
    if not caregiver:
        return []
    patients = caregiver.patients  # relationship via association
    return patients

def get_patient_summary(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        return None
    # Get all sessions
    sessions = db.query(GameSession).filter(GameSession.patient_id == patient_id).all()
    total_games = len(sessions)
    category_accs = defaultdict(list)
    for s in sessions:
        if s.accuracy is not None:
            game = db.query(Game).filter(Game.id == s.game_id).first()
            if game:
                category_accs[game.category].append(s.accuracy)
    category_scores = {}
    for cat, accs in category_accs.items():
        category_scores[cat] = round(sum(accs) / len(accs) * 100, 2)
    overall = round(sum(category_scores.values()) / len(category_scores), 2) if category_scores else 0.0

    # Current streak (consecutive days with at least one session)
    # We'll compute simple streak by checking distinct dates in descending order.
    import datetime
    dates = set()
    for s in sessions:
        if s.created_at:
            dates.add(s.created_at.date())
    if not dates:
        streak = 0
    else:
        sorted_dates = sorted(dates, reverse=True)
        streak = 1
        prev = sorted_dates[0]
        for d in sorted_dates[1:]:
            if (prev - d).days == 1:
                streak += 1
                prev = d
            else:
                break
    return {
        "patient_id": patient.id,
        "name": patient.user.full_name,
        "email": patient.user.email,
        "overall_performance": overall,
        "category_scores": category_scores,
        "games_completed": total_games,
        "current_streak_days": streak,
    }

def get_caregiver_dashboard(db: Session, caregiver_user_id: int):
    patients = get_caregiver_patients(db, caregiver_user_id)
    result = []
    for p in patients:
        summary = get_patient_summary(db, p.id)
        if summary:
            result.append(summary)
    return result
