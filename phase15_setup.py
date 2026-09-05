from pathlib import Path

# 1. Create adaptive_service.py
service_content = '''from sqlalchemy.orm import Session
from app.models.game_session import GameSession

DIFFICULTY_ORDER = ["easy", "medium", "hard"]

def get_latest_difficulty(db: Session, patient_id: int, game_id: int):
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
    return "easy"

def get_recent_accuracy(db: Session, patient_id: int, game_id: int, n=5):
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

def recommend_difficulty(db: Session, patient_id: int, game_id: int):
    current_difficulty = get_latest_difficulty(db, patient_id, game_id)
    avg_accuracy = get_recent_accuracy(db, patient_id, game_id)
    if avg_accuracy is None:
        return {
            "recommended_difficulty": current_difficulty,
            "reason": "Not enough data to adjust difficulty."
        }
    if avg_accuracy > 0.85:
        if current_difficulty == "easy":
            new_diff = "medium"
        elif current_difficulty == "medium":
            new_diff = "hard"
        else:
            new_diff = current_difficulty
        reason = f"High accuracy ({avg_accuracy:.2f}), increasing difficulty from {current_difficulty} to {new_diff}"
    elif avg_accuracy < 0.60:
        if current_difficulty == "hard":
            new_diff = "medium"
        elif current_difficulty == "medium":
            new_diff = "easy"
        else:
            new_diff = current_difficulty
        reason = f"Low accuracy ({avg_accuracy:.2f}), decreasing difficulty from {current_difficulty} to {new_diff}"
    else:
        new_diff = current_difficulty
        reason = f"Moderate accuracy ({avg_accuracy:.2f}), keeping difficulty at {current_difficulty}"
    return {
        "recommended_difficulty": new_diff,
        "reason": reason
    }
'''

path = Path("backend/app/services/adaptive_service.py")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(service_content.strip(), encoding='utf-8')
print("Created adaptive_service.py")

# 2. Create recommendations API
api_content = '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.adaptive_service import recommend_difficulty

router = APIRouter()

@router.get("/difficulty/{patient_id}/{game_id}")
def get_recommended_difficulty(
    patient_id: int,
    game_id: int,
    db: Session = Depends(get_db)
):
    return recommend_difficulty(db, patient_id, game_id)
'''

path = Path("backend/app/api/recommendations.py")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(api_content.strip(), encoding='utf-8')
print("Created recommendations.py")

# 3. Update main.py to include recommendations router
main_content = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app import models  # noqa: F401
from app.api import auth, games, performance, recommendations

app = FastAPI(title="Cognitive Gaming API")

# Permissive CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()
    print("Database initialized")

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(games.router, prefix="/api/games", tags=["games"])
app.include_router(performance.router, prefix="/api/performance", tags=["performance"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])

@app.get("/")
def read_root():
    return {"message": "Cognitive Gaming API is running"}
'''

path = Path("backend/app/main.py")
path.write_text(main_content.strip(), encoding='utf-8')
print("Updated main.py")
