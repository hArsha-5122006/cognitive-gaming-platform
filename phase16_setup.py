from pathlib import Path

# 1. Create ai/models/train.py
train_content = '''import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

def load_data():
    # Try to find features.csv in possible locations
    candidates = [
        Path("ai/data/features.csv"),
        Path("backend/ai/data/features.csv"),
    ]
    for path in candidates:
        if path.exists():
            return pd.read_csv(path)
    raise FileNotFoundError("features.csv not found. Run feature engineering first.")

def main():
    df = load_data()
    print(f"Loaded {len(df)} records")

    # Define feature columns and target
    feature_cols = [
        'average_accuracy', 'average_reaction_time_ms', 'mistake_rate',
        'completion_rate', 'average_score', 'total_attempts', 'total_mistakes'
    ]
    target_col = 'current_difficulty'

    # Filter rows with valid target
    df = df.dropna(subset=[target_col])
    X = df[feature_cols].fillna(0)
    y = df[target_col]

    # Encode target labels (easy=0, medium=1, hard=2)
    difficulty_map = {'easy': 0, 'medium': 1, 'hard': 2}
    y_encoded = y.map(difficulty_map)

    if len(X) < 5:
        print("Not enough data to train; need at least 5 samples.")
        return

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )

    # Train XGBoost
    model = XGBClassifier(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        use_label_encoder=False,
        eval_metric='mlogloss'
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc:.2f}")
    print(classification_report(y_test, y_pred))

    # Save model
    output_dir = Path("ai/saved_models")
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "difficulty_model.pkl"
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    main()
'''

path = Path("ai/models/train.py")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(train_content.strip(), encoding='utf-8')
print("Created ai/models/train.py")

# 2. Create ai/models/predict.py
predict_content = '''import joblib
from pathlib import Path

DIFFICULTY_MAP = {0: 'easy', 1: 'medium', 2: 'hard'}

MODEL_PATH = Path("ai/saved_models/difficulty_model.pkl")

_model = None

def load_model():
    global _model
    if _model is None and MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    return _model

def predict_difficulty(features):
    model = load_model()
    if model is None:
        return None
    # Expect features as list in order:
    # [average_accuracy, average_reaction_time_ms, mistake_rate, completion_rate, average_score, total_attempts, total_mistakes]
    import numpy as np
    X = np.array([features])
    pred = model.predict(X)[0]
    return DIFFICULTY_MAP[int(pred)]
'''

path = Path("ai/models/predict.py")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(predict_content.strip(), encoding='utf-8')
print("Created ai/models/predict.py")

# 3. Update backend/app/services/adaptive_service.py to use ML if available
adaptive_content = '''from sqlalchemy.orm import Session
from app.models.game_session import GameSession
import sys
from pathlib import Path

# Add ai/models to path if running in backend container
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
    # Compute features for ML model from recent sessions
    sessions = (
        db.query(GameSession)
        .filter(
            GameSession.patient_id == patient_id,
            GameSession.game_id == game_id
        )
        .order_by(GameSession.created_at.desc())
        .limit(10)
        .all()
    )
    if not sessions:
        return None
    accs = [s.accuracy for s in sessions if s.accuracy is not None]
    times = [s.time_taken_seconds for s in sessions if s.time_taken_seconds is not None]
    mistakes = [s.mistakes for s in sessions if s.mistakes is not None]
    attempts = [s.attempts for s in sessions if s.attempts is not None]
    scores = [s.score for s in sessions if s.score is not None]
    # Compute averages
    avg_acc = sum(accs)/len(accs) if accs else 0
    avg_reaction = 0  # We don't track per-session avg reaction easily; skip or approximate
    avg_time = sum(times)/len(times) if times else 0
    total_attempts = sum(attempts)
    total_mistakes = sum(mistakes)
    mistake_rate = total_mistakes/total_attempts if total_attempts else 0
    completion_rate = sum(1 for s in sessions if s.status == 'completed') / len(sessions)
    avg_score = sum(scores)/len(scores) if scores else 0
    return [
        avg_acc, avg_reaction, mistake_rate, completion_rate, avg_score,
        total_attempts, total_mistakes
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
    except Exception:
        pass  # Fall back to rule-based

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
path.write_text(adaptive_content.strip(), encoding='utf-8')
print("Updated adaptive_service.py with ML integration")
