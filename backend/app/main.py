from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app import models  # noqa: F401
from app.api import auth, games, performance

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

@app.get("/")
def read_root():
    return {"message": "Cognitive Gaming API is running"}
