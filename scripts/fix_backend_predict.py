from pathlib import Path

content = '''import pickle
from pathlib import Path

MODEL_PATH = Path("ai/saved_models/difficulty_model.pkl")
_model_data = None

def load_model_data():
    global _model_data
    if _model_data is None and MODEL_PATH.exists():
        with open(MODEL_PATH, "rb") as f:
            _model_data = pickle.load(f)
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
'''

path = Path("backend/ai/models/predict.py")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(content.strip(), encoding='utf-8')
print("backend/ai/models/predict.py now uses pickle.")
