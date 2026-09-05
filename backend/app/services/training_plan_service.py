from sqlalchemy.orm import Session
from collections import defaultdict
from app.models.game_session import GameSession
from app.models.game import Game

# Emoji mapping for categories (fallback)
CATEGORY_EMOJI = {
    "memory": "🧠",
    "attention": "🎯",
    "sequence": "🔢",
    "pattern": "🔷",
    "reaction": "⚡",
    "language": "📝"
}

DEFAULT_PLAN = [
    {"category": "memory", "duration": 5},
    {"category": "attention", "duration": 5},
    {"category": "pattern", "duration": 5},
    {"category": "reaction", "duration": 3},
]

def get_category_accuracies(db: Session, patient_id: int):
    sessions = (
        db.query(GameSession, Game.category)
        .join(Game, GameSession.game_id == Game.id)
        .filter(GameSession.patient_id == patient_id)
        .all()
    )
    if not sessions:
        return {}
    category_accs = defaultdict(list)
    for session, category in sessions:
        if session.accuracy is not None:
            category_accs[category].append(session.accuracy)
    avg_accs = {}
    for cat, accs in category_accs.items():
        avg_accs[cat] = sum(accs) / len(accs)
    return avg_accs

def generate_training_plan(db: Session, patient_id: int):
    accs = get_category_accuracies(db, patient_id)
    if not accs:
        # Default plan for new patient
        plan = DEFAULT_PLAN.copy()
        reason = "No performance data yet. Using default balanced plan."
    else:
        # Sort categories by accuracy ascending (weakest first)
        sorted_cats = sorted(accs.items(), key=lambda x: x[1])
        # Allocate durations based on rank
        # We'll use a simple mapping: first (weakest) = 8 min, second = 6, third = 4, others = 3
        # For categories not present, default 5 min
        plan = []
        for idx, (cat, acc) in enumerate(sorted_cats):
            if idx == 0:
                duration = 8
            elif idx == 1:
                duration = 6
            elif idx == 2:
                duration = 4
            else:
                duration = 3
            plan.append({"category": cat, "duration": duration})
        # Add missing categories with default durations
        all_categories = set(CATEGORY_EMOJI.keys())
        present_cats = {item["category"] for item in plan}
        for cat in all_categories - present_cats:
            plan.append({"category": cat, "duration": 5})
        reason = "Plan adjusted based on performance (weaker areas get more time)."

    # Map to game details (id, name, emoji)
    plan_with_games = []
    for item in plan:
        cat = item["category"]
        # Find an active game for this category
        game = db.query(Game).filter(Game.category == cat, Game.is_active == 1).first()
        if game:
            plan_with_games.append({
                "game_id": game.id,
                "name": game.name,
                "category": cat,
                "emoji": CATEGORY_EMOJI.get(cat, "🎮"),
                "duration_minutes": item["duration"]
            })
    # Calculate total time
    total = sum(item["duration_minutes"] for item in plan_with_games)
    return {
        "patient_id": patient_id,
        "reason": reason,
        "total_minutes": total,
        "plan": plan_with_games
    }