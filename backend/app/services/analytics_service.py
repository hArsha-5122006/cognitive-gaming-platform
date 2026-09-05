from sqlalchemy.orm import Session
from collections import defaultdict
from app.models.game_session import GameSession
from app.models.game import Game

def get_patient_analytics(db: Session, patient_id: int):
    sessions = (
        db.query(GameSession, Game.name, Game.category)
        .join(Game, GameSession.game_id == Game.id)
        .filter(GameSession.patient_id == patient_id)
        .order_by(GameSession.created_at.asc())
        .all()
    )
    if not sessions:
        return {"patient_id": patient_id, "sessions": [], "trend": [], "category_trend": {}}

    # Group by date
    date_groups = defaultdict(list)
    for s, gname, cat in sessions:
        date_str = s.created_at.strftime("%Y-%m-%d") if s.created_at else "unknown"
        date_groups[date_str].append({
            "game_id": s.game_id,
            "game_name": gname,
            "category": cat,
            "accuracy": s.accuracy,
            "score": s.score,
            "time_taken_seconds": s.time_taken_seconds,
            "difficulty": s.difficulty_level,
        })

    # Build per-date accuracy average
    trend = []
    for date_str in sorted(date_groups.keys()):
        accs = [item["accuracy"] for item in date_groups[date_str] if item["accuracy"] is not None]
        if accs:
            avg_acc = sum(accs) / len(accs) * 100
        else:
            avg_acc = 0
        trend.append({
            "date": date_str,
            "accuracy": round(avg_acc, 2),
            "sessions_count": len(date_groups[date_str]),
        })

    # Category trend (average accuracy per category over all sessions)
    category_accs = defaultdict(list)
    for s, gname, cat in sessions:
        if s.accuracy is not None:
            category_accs[cat].append(s.accuracy)
    category_trend = {}
    for cat, accs in category_accs.items():
        category_trend[cat] = round(sum(accs) / len(accs) * 100, 2)

    return {
        "patient_id": patient_id,
        "sessions": [
            {
                "date": s.created_at.strftime("%Y-%m-%d") if s.created_at else "unknown",
                "game_name": gname,
                "category": cat,
                "accuracy": s.accuracy,
                "score": s.score,
                "time_taken_seconds": s.time_taken_seconds,
                "difficulty": s.difficulty_level,
            }
            for s, gname, cat in sessions
        ],
        "trend": trend,
        "category_trend": category_trend,
    }
