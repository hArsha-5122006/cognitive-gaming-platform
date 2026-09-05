import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from xgboost import XGBClassifier
import joblib

def load_data():
    candidates = [
        Path("ai/data"),
        Path("backend/ai/data")
    ]
    for base in candidates:
        sessions_path = base / "game_sessions.csv"
        results_path = base / "game_results.csv"
        if sessions_path.exists() and results_path.exists():
            print(f"Loading data from {base}")
            sessions = pd.read_csv(sessions_path)
            results = pd.read_csv(results_path)
            return sessions, results
    raise FileNotFoundError("game_sessions.csv or game_results.csv not found. Run export first.")

def engineer_features(sessions, results):
    # Aggregate results per session to get average reaction time
    if not results.empty:
        reaction_agg = results.groupby('session_id')['reaction_time_ms'].mean().reset_index()
        reaction_agg.columns = ['session_id', 'avg_reaction_time_ms']
        # Sessions table has 'id' as session identifier
        sessions = sessions.merge(reaction_agg, left_on='id', right_on='session_id', how='left')
        sessions['avg_reaction_time_ms'] = sessions['avg_reaction_time_ms'].fillna(0)
    else:
        sessions['avg_reaction_time_ms'] = 0

    # Sort by created_at to compute previous scores and trends
    sessions['created_at'] = pd.to_datetime(sessions['created_at'])
    sessions = sessions.sort_values(['patient_id', 'created_at'])

    # Group by patient to get previous accuracy
    sessions['previous_accuracy'] = sessions.groupby('patient_id')['accuracy'].shift(1).fillna(sessions['accuracy'])
    sessions['previous_score'] = sessions.groupby('patient_id')['score'].shift(1).fillna(sessions['score'])

    # Performance trend: difference between current and previous accuracy
    sessions['performance_trend'] = sessions['accuracy'] - sessions['previous_accuracy']

    # Encode difficulty to numeric target
    difficulty_map = {'easy': 0, 'medium': 1, 'hard': 2}
    sessions['target_difficulty'] = sessions['difficulty_level'].map(difficulty_map)

    # Drop rows without target
    sessions = sessions.dropna(subset=['target_difficulty'])

    # Feature columns
    feature_cols = [
        'accuracy', 'avg_reaction_time_ms', 'mistakes', 'score',
        'previous_accuracy', 'previous_score', 'performance_trend',
        'time_taken_seconds', 'attempts'
    ]
    X = sessions[feature_cols].fillna(0)
    y = sessions['target_difficulty'].astype(int)

    return X, y, feature_cols, difficulty_map

def main():
    sessions, results = load_data()
    print(f"Loaded {len(sessions)} sessions and {len(results)} results")

    if len(sessions) < 10:
        print("Warning: Very few sessions. Model may not generalize well.")

    X, y, feature_cols, difficulty_map = engineer_features(sessions, results)

    # Train/test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train XGBoost
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
        use_label_encoder=False,
        eval_metric='mlogloss'
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
    print(f"Test Accuracy: {acc:.3f}")
    print(f"Precision: {precision:.3f}, Recall: {recall:.3f}, F1: {f1:.3f}")
    print(classification_report(y_test, y_pred))

    # Save model and feature info
    output_dir = Path("ai/saved_models")
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "difficulty_model.pkl"
    joblib.dump({
        'model': model,
        'feature_cols': feature_cols,
        'difficulty_map': difficulty_map,
        'reverse_map': {v: k for k, v in difficulty_map.items()}
    }, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    main()