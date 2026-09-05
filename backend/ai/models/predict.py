import joblib
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