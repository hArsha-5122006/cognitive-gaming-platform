from pathlib import Path

content = '''import csv
import psycopg2
from pathlib import Path

# Inside container, use service name 'db'
conn = psycopg2.connect(
    host="db",
    port=5432,
    user="cognitive_user",
    password="cognitive_pass",
    database="cognitive_db"
)
cursor = conn.cursor()

output_dir = Path("ai/data")
output_dir.mkdir(parents=True, exist_ok=True)

cursor.execute("SELECT * FROM game_sessions")
sessions = cursor.fetchall()
session_columns = [desc[0] for desc in cursor.description]
with open(output_dir / "game_sessions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(session_columns)
    writer.writerows(sessions)

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
'''

path = Path("backend/export_data.py")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(content.strip(), encoding='utf-8')
print("backend/export_data.py updated with db host.")
