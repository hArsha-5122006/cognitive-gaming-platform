from pathlib import Path

content = '''from sqlalchemy.orm import Session
from app.models.game_session import GameSession
import sys
from pathlib import Path

sys.path.append('/app/ai/models')
sys.path.append('/app')

def get_latest_difficulty(db, patient_id, game_id):
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
    return 'easy'

def get_recent_accuracy(db, patient_id, game_id, n=5):
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

def get_ml_features(db, patient_id, game_id):
    # Get sessions for this patient and game, ordered by time
    sessions = (
        db.query(GameSession)
        .filter(
            GameSession.patient_id == patient_id,
            GameSession.game_id == game_id
        )
        .order_by(GameSession.created_at.asc())
        .all()
    )
    if not sessions:
        return None

    # Latest session as current
    latest = sessions[-1]
    # Previous sessions (exclude latest)
    prev_sessions = sessions[:-1]

    # Helper to compute mean of attribute
    def mean_attr(attr, sess_list):
        vals = [getattr(s, attr) for s in sess_list if getattr(s, attr) is not None]
        return sum(vals) / len(vals) if vals else 0.0

    current_accuracy = latest.accuracy if latest.accuracy is not None else 0.0
    current_score = latest.score if latest.score is not None else 0.0
    current_mistakes = latest.mistakes if latest.mistakes is not None else 0
    current_attempts = latest.attempts if latest.attempts is not None else 0
    current_time = latest.time_taken_seconds if latest.time_taken_seconds is not None else 0.0

    prev_accuracy = mean_attr('accuracy', prev_sessions)
    prev_score = mean_attr('score', prev_sessions)

    # average reaction time: from latest session? we'll approximate using time_taken / attempts
    if current_attempts > 0:
        avg_reaction = current_time / current_attempts
    else:
        avg_reaction = 0.0

    performance_trend = current_accuracy - prev_accuracy

    # Feature order must match training:
    # ['accuracy', 'avg_reaction_time_ms', 'mistakes', 'score',
    #  'previous_accuracy', 'previous_score', 'performance_trend',
    #  'time_taken_seconds', 'attempts']
    return [
        current_accuracy,
        avg_reaction,
        current_mistakes,
        current_score,
        prev_accuracy,
        prev_score,
        performance_trend,
        current_time,
        current_attempts
    ]

def recommend_difficulty(db, patient_id, game_id):
    current_difficulty = get_latest_difficulty(db, patient_id, game_id)
    avg_accuracy = get_recent_accuracy(db, patient_id, game_id)

    # Try ML model first if possible
    try:
        from predict import predict_difficulty
        features = get_ml_features(db, patient_id, game_id)
        if features is not None:
            ml_recommendation = predict_difficulty(features)
            if ml_recommendation:
                reason = f"ML model recommended {ml_recommendation} based on performance features."
                return {
                    "recommended_difficulty": ml_recommendation,
                    "reason": reason,
                    "source": "ml"
                }
    except Exception as e:
        print(f"ML recommendation failed: {e}")

    # Rule-based fallback
    if avg_accuracy is None:
        return {
            "recommended_difficulty": current_difficulty,
            "reason": "Not enough data.",
            "source": "rule"
        }
    if avg_accuracy > 0.85:
        if current_difficulty == 'easy':
            new_diff = 'medium'
        elif current_difficulty == 'medium':
            new_diff = 'hard'
        else:
            new_diff = current_difficulty
        reason = f"High accuracy ({avg_accuracy:.2f}), increasing difficulty from {current_difficulty} to {new_diff}"
    elif avg_accuracy < 0.60:
        if current_difficulty == 'hard':
            new_diff = 'medium'
        elif current_difficulty == 'medium':
            new_diff = 'easy'
        else:
            new_diff = current_difficulty
        reason = f"Low accuracy ({avg_accuracy:.2f}), decreasing difficulty from {current_difficulty} to {new_diff}"
    else:
        new_diff = current_difficulty
        reason = f"Moderate accuracy ({avg_accuracy:.2f}), keeping difficulty at {current_difficulty}"
    return {
        "recommended_difficulty": new_diff,
        "reason": reason,
        "source": "rule"
    }
'''

path = Path("backend/app/services/adaptive_service.py")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(content.strip(), encoding='utf-8')
print("adaptive_service.py fixed!")
