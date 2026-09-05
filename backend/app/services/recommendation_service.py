from sqlalchemy.orm import Session
from collections import defaultdict
from app.models.game_session import GameSession
from app.models.game import Game

def get_weakest_category(db: Session, patient_id: int):
    """Return the category with lowest average accuracy for patient."""
    sessions = (
        db.query(GameSession, Game.category)
        .join(Game, GameSession.game_id == Game.id)
        .filter(GameSession.patient_id == patient_id)
        .all()
    )
    if not sessions:
        return None

    category_accs = defaultdict(list)
    for session, category in sessions:
        if session.accuracy is not None:
            category_accs[category].append(session.accuracy)

    if not category_accs:
        return None

    # Compute average accuracy per category
    avg_accs = {}
    for cat, accs in category_accs.items():
        avg_accs[cat] = sum(accs) / len(accs)

    # Find category with lowest average
    weakest = min(avg_accs, key=avg_accs.get)
    return weakest, avg_accs[weakest], avg_accs

def recommend_next_game(db: Session, patient_id: int):
    weakest_info = get_weakest_category(db, patient_id)
    if not weakest_info:
        # Default to Memory Game (id=1)
        return {
            "patient_id": patient_id,
            "recommended_game_id": 1,
            "recommended_category": "memory",
            "reason": "No gameplay data yet. Starting with Memory Game.",
            "category_accuracies": {}
        }
    weakest_cat, weakest_acc, all_accs = weakest_info
    # Find an active game for that category
    game = db.query(Game).filter(Game.category == weakest_cat, Game.is_active == 1).first()
    if not game:
        game = db.query(Game).first()
    return {
        "patient_id": patient_id,
        "recommended_game_id": game.id,
        "recommended_category": weakest_cat,
        "reason": f"Lowest performance in {weakest_cat} ({weakest_acc:.2f} accuracy).",
        "category_accuracies": all_accs
    }