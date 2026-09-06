from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db, SessionLocal
from app import models  # noqa: F401
from app.api import auth, games, performance, recommendations, reminders, caregivers, daily_routine
from app.models.patient import Patient
from app.models.daily_routine import DailyRoutineItem

app = FastAPI(title="Cognitive Gaming API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def seed_default_daily_routines():
    db = SessionLocal()
    try:
        patients = db.query(Patient).all()
        default_routines = [
            {"title": "Morning Wake-up", "scheduled_time": "7:00 AM"},
            {"title": "Breakfast", "scheduled_time": "8:00 AM"},
            {"title": "Medicine", "scheduled_time": "10:00 AM"},
            {"title": "Drink Water", "scheduled_time": "12:00 PM"},
            {"title": "Lunch", "scheduled_time": "1:00 PM"},
            {"title": "Walk", "scheduled_time": "5:00 PM"},
            {"title": "Dinner", "scheduled_time": "8:00 PM"},
            {"title": "Sleep", "scheduled_time": "10:00 PM"},
        ]
        for patient in patients:
            existing_count = db.query(DailyRoutineItem).filter(
                DailyRoutineItem.patient_id == patient.id
            ).count()
            if existing_count == 0:
                for item in default_routines:
                    db.add(DailyRoutineItem(
                        patient_id=patient.id,
                        title=item["title"],
                        scheduled_time=item["scheduled_time"]
                    ))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    init_db()
    seed_default_daily_routines()
    print("Database initialized and seeded")

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(games.router, prefix="/api/games", tags=["games"])
app.include_router(performance.router, prefix="/api/performance", tags=["performance"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["reminders"])
app.include_router(caregivers.router, prefix="/api/caregivers", tags=["caregivers"])
app.include_router(daily_routine.router, prefix="/api/daily-routine", tags=["daily-routine"])

@app.get("/")
def read_root():
    return {"message": "Cognitive Gaming API is running"}
