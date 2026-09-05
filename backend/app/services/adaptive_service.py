from sqlalchemy.orm import Session
from app.models.game_session import GameSession

DIFFICULTY_ORDER = ["easy", "medium", "hard"]

def get_latest_difficulty(db: Session, patient_id: int, game_id: int):
    session = (
        db.query(GameSession)
        .filter(
            GameSession.patient_id == patient_id,
            GameSession.game_id == game_id
        )
        .order_by(GameSession.created_at.desc())
        .first()
    )
    if session and session.difficulty_level:
        return session.difficulty_level
    return "easy"

def get_recent_accuracy(db: Session, patient_id: int, game_id: int, n=5):
    sessions = (
        db.query(GameSession)
        .filter(
            GameSession.patient_id == patient_id,
            GameSession.game_id == game_id
        )
        .order_by(GameSession.created_at.desc())
        .limit(n)
        .all()
    )
    if not sessions:
        return None
    accs = [s.accuracy for s in sessions if s.accuracy is not None]
    if not accs:
        return None
    return sum(accs) / len(accs)

def recommend_difficulty(db: Session, patient_id: int, game_id: int):
    current_difficulty = get_latest_difficulty(db, patient_id, game_id)
    avg_accuracy = get_recent_accuracy(db, patient_id, game_id)
    if avg_accuracy is None:
        return {
            "recommended_difficulty": current_difficulty,
            "reason": "Not enough data to adjust difficulty."
        }
    if avg_accuracy > 0.85:
        if current_difficulty == "easy":
            new_diff = "medium"
        elif current_difficulty == "medium":
            new_diff = "hard"
        else:
            new_diff = current_difficulty
        reason = f"High accuracy ({avg_accuracy:.2f}), increasing difficulty from {current_difficulty} to {new_diff}"
    elif avg_accuracy < 0.60:
        if current_difficulty == "hard":
            new_diff = "medium"
        elif current_difficulty == "medium":
            new_diff = "easy"
        else:
            new_diff = current_difficulty
        reason = f"Low accuracy ({avg_accuracy:.2f}), decreasing difficulty from {current_difficulty} to {new_diff}"
    else:
        new_diff = current_difficulty
        reason = f"Moderate accuracy ({avg_accuracy:.2f}), keeping difficulty at {current_difficulty}"
    return {
        "recommended_difficulty": new_diff,
        "reason": reason
    }