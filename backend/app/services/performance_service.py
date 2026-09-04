from sqlalchemy.orm import Session
from collections import defaultdict
from app.models.game_session import GameSession
from app.models.game import Game

def calculate_cognitive_scores(db: Session, patient_id: int):
    """
    Calculate cognitive scores per game category and overall.
    Returns a dictionary with category scores (0-100) and overall.
    """
    # Get all sessions for patient joined with game category
    sessions = (
        db.query(GameSession, Game.category)
        .join(Game, GameSession.game_id == Game.id)
        .filter(GameSession.patient_id == patient_id)
        .all()
    )
    if not sessions:
        return {
            "patient_id": patient_id,
            "scores": {},
            "overall": 0.0,
            "message": "No game data available"
        }

    category_accuracies = defaultdict(list)
    category_scores = {}

    for session, category in sessions:
        if session.accuracy is not None:
            category_accuracies[category].append(session.accuracy)

    # Convert accuracy (0-1) to score (0-100)
    for cat, accs in category_accuracies.items():
        avg_acc = sum(accs) / len(accs)
        category_scores[cat] = round(avg_acc * 100, 2)

    # Overall score = average of category scores
    if category_scores:
        overall = round(sum(category_scores.values()) / len(category_scores), 2)
    else:
        overall = 0.0

    return {
        "patient_id": patient_id,
        "scores": category_scores,
        "overall": overall,
        "note": "Game-based performance indicator, not a medical diagnosis."
    }
