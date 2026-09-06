import csv
import psycopg2
from pathlib import Path

# Database connection parameters (same as docker-compose)
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="cognitive_user",
    password="cognitive_pass",
    database="cognitive_db"
)
cursor = conn.cursor()

# Create output directory
output_dir = Path("ai/data")
output_dir.mkdir(parents=True, exist_ok=True)

# Export game_sessions
cursor.execute("SELECT * FROM game_sessions")
sessions = cursor.fetchall()
session_columns = [desc[0] for desc in cursor.description]
with open(output_dir / "game_sessions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(session_columns)
    writer.writerows(sessions)

# Export game_results
cursor.execute("SELECT * FROM game_results")
results = cursor.fetchall()
result_columns = [desc[0] for desc in cursor.description]
with open(output_dir / "game_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(result_columns)
    writer.writerows(results)

print(f"Exported {len(sessions)} sessions and {len(results)} results to {output_dir}")

cursor.close()
conn.close()
