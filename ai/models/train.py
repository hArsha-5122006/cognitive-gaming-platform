import pandas as pd
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