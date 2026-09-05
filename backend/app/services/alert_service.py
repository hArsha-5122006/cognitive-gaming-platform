from sqlalchemy.orm import Session
from datetime import datetime, timezone
from collections import defaultdict
from app.models.game_session import GameSession
from app.models.game import Game
from app.models.reminder import Reminder

def generate_caregiver_alerts(db: Session, patient_id: int):
    alerts = []

    # 1. Performance changes per category
    sessions = (
        db.query(GameSession, Game.category)
        .join(Game, GameSession.game_id == Game.id)
        .filter(GameSession.patient_id == patient_id)
        .order_by(GameSession.created_at.asc())
        .all()
    )
    if sessions:
        category_accs = defaultdict(list)
        for s, cat in sessions:
            if s.accuracy is not None:
                category_accs[cat].append(s.accuracy)

        for cat, accs in category_accs.items():
            if len(accs) >= 3:
                recent = sum(accs[-3:]) / 3
                previous = sum(accs[:-3]) / len(accs[:-3]) if len(accs[:-3]) > 0 else recent
                if recent < previous - 0.15:
                    alerts.append({
                        "type": "warning",
                        "message": f"Attention: {cat.capitalize()} performance decreased compared to recent sessions."
                    })
                elif recent > previous + 0.15:
                    alerts.append({
                        "type": "success",
                        "message": f"Good news: {cat.capitalize()} performance is improving."
                    })
            elif len(accs) == 2:
                if accs[-1] < accs[0] - 0.2:
                    alerts.append({
                        "type": "warning",
                        "message": f"Attention: {cat.capitalize()} performance decreased compared to earlier."
                    })
                elif accs[-1] > accs[0] + 0.2:
                    alerts.append({
                        "type": "success",
                        "message": f"Good news: {cat.capitalize()} performance is improving."
                    })

    # 2. Missed reminders (scheduled time passed, not completed)
    now = datetime.now(timezone.utc)
    missed_reminders = (
        db.query(Reminder)
        .filter(
            Reminder.patient_id == patient_id,
            Reminder.is_completed == False,
            Reminder.scheduled_time < now
        )
        .count()
    )
    if missed_reminders > 0:
        alerts.append({
            "type": "warning",
            "message": f"Patient missed {missed_reminders} scheduled activities or reminders."
        })

    return alerts
