import joblib
from pathlib import Path

MODEL_PATH = Path("ai/saved_models/difficulty_model.pkl")
_model_data = None

def load_model_data():
    global _model_data
    if _model_data is None and MODEL_PATH.exists():
        _model_data = joblib.load(MODEL_PATH)
    return _model_data

def predict_difficulty(features):
    data = load_model_data()
    if data is None:
        return None
    model = data['model']
    reverse_map = data['reverse_map']
    X = [features]
    pred = model.predict(X)[0]
    return reverse_map[int(pred)]