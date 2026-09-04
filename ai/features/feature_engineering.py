import csv
import statistics
from collections import defaultdict
from pathlib import Path

def read_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def find_data_dir():
    candidates = [
        Path("ai/data"),
        Path("backend/ai/data"),
    ]
    for d in candidates:
        if (d / "game_sessions.csv").exists() and (d / "game_results.csv").exists():
            return d
    raise FileNotFoundError("CSV files not found. Run the export script first.")

def compute_features():
    data_dir = find_data_dir()
    sessions = read_csv(data_dir / "game_sessions.csv")
    results = read_csv(data_dir / "game_results.csv")

    results_by_session = defaultdict(list)
    for r in results:
        sid = safe_int(r.get("session_id"))
        results_by_session[sid].append(r)

    sessions_by_patient = defaultdict(list)
    for s in sessions:
        pid = safe_int(s.get("patient_id"))
        sessions_by_patient[pid].append(s)

    features = []
    for patient_id, patient_sessions in sessions_by_patient.items():
        patient_sessions.sort(key=lambda x: x.get("created_at") or x.get("start_time") or "")

        total_attempts = sum(safe_int(s.get("attempts")) for s in patient_sessions)
        total_mistakes = sum(safe_int(s.get("mistakes")) for s in patient_sessions)
        total_score = sum(safe_float(s.get("score")) for s in patient_sessions)
        total_time = sum(safe_float(s.get("time_taken_seconds")) for s in patient_sessions)

        accuracies = [safe_float(s.get("accuracy")) for s in patient_sessions]
        reaction_times = []
        for s in patient_sessions:
            sid = safe_int(s.get("id"))
            session_results = results_by_session.get(sid, [])
            times = [safe_float(r.get("reaction_time_ms"), 0.0) for r in session_results if safe_float(r.get("reaction_time_ms"), 0.0) > 0]
            if times:
                reaction_times.append(statistics.mean(times))

        avg_reaction_time = statistics.mean(reaction_times) if reaction_times else 0.0
        mistake_rate = total_mistakes / total_attempts if total_attempts > 0 else 0.0
        completion_rate = sum(1 for s in patient_sessions if s.get("status") == "completed") / len(patient_sessions) if patient_sessions else 0.0
        avg_accuracy = statistics.mean(accuracies) if accuracies else 0.0
        avg_score = total_score / len(patient_sessions) if patient_sessions else 0.0

        current_difficulty = patient_sessions[-1].get("difficulty_level", "easy") if patient_sessions else "easy"

        if len(patient_sessions) > 1:
            prev_acc = statistics.mean(accuracies[:-1])
        else:
            prev_acc = avg_accuracy

        recent_accs = accuracies[-3:] if accuracies else []
        recent_accuracy = statistics.mean(recent_accs) if recent_accs else avg_accuracy

        if recent_accuracy > prev_acc + 0.05:
            trend = "improving"
        elif recent_accuracy < prev_acc - 0.05:
            trend = "declining"
        else:
            trend = "stable"

        features.append({
            "patient_id": patient_id,
            "total_sessions": len(patient_sessions),
            "total_attempts": total_attempts,
            "total_mistakes": total_mistakes,
            "total_score": round(total_score, 2),
            "total_time_taken_seconds": round(total_time, 2),
            "average_accuracy": round(avg_accuracy, 4),
            "average_reaction_time_ms": round(avg_reaction_time, 2),
            "mistake_rate": round(mistake_rate, 4),
            "completion_rate": round(completion_rate, 4),
            "average_score": round(avg_score, 2),
            "current_difficulty": current_difficulty,
            "previous_accuracy": round(prev_acc, 4),
            "recent_accuracy": round(recent_accuracy, 4),
            "performance_trend": trend,
        })

    output_dir = Path("ai/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "features.csv"
    fieldnames = list(features[0].keys()) if features else ["patient_id","total_sessions","total_attempts","total_mistakes","total_score","total_time_taken_seconds","average_accuracy","average_reaction_time_ms","mistake_rate","completion_rate","average_score","current_difficulty","previous_accuracy","recent_accuracy","performance_trend"]
    with open(output_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        if features:
            writer.writerows(features)
    print(f"Features saved to {output_path}")

if __name__ == "__main__":
    compute_features()
