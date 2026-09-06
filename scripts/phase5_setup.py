from pathlib import Path

# Define all file paths and contents
files = {
    "backend/app/schemas/game.py": '''from pydantic import BaseModel
from typing import Optional, List

class GameResultItem(BaseModel):
    question: Optional[str] = None
    correct_answer: Optional[str] = None
    user_answer: Optional[str] = None
    is_correct: int  # 0 or 1
    reaction_time_ms: Optional[float] = None

class GameResultSubmit(BaseModel):
    game_id: int
    score: float
    accuracy: float
    time_taken_seconds: float
    mistakes: int
    attempts: int
    difficulty_level: str
    results: Optional[List[GameResultItem]] = None
''',

    "backend/app/services/game_service.py": '''from sqlalchemy.orm import Session
from app.models.game_session import GameSession
from app.models.game_result import GameResult
from app.schemas.game import GameResultSubmit

def save_game_result(db: Session, patient_id: int, data: GameResultSubmit):
    # Create GameSession
    session = GameSession(
        patient_id=patient_id,
        game_id=data.game_id,
        score=data.score,
        accuracy=data.accuracy,
        time_taken_seconds=data.time_taken_seconds,
        mistakes=data.mistakes,
        attempts=data.attempts,
        difficulty_level=data.difficulty_level,
        status="completed"
    )
    db.add(session)
    db.flush()  # to get session.id

    # Optionally save individual results
    if data.results:
        for item in data.results:
            result = GameResult(
                session_id=session.id,
                question=item.question,
                correct_answer=item.correct_answer,
                user_answer=item.user_answer,
                is_correct=item.is_correct,
                reaction_time_ms=item.reaction_time_ms
            )
            db.add(result)

    db.commit()
    db.refresh(session)
    return session
''',

    "backend/app/api/games.py": '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.patient import Patient
from app.schemas.game import GameResultSubmit
from app.services.game_service import save_game_result

router = APIRouter()

@router.post("/submit_result", status_code=201)
def submit_game_result(
    data: GameResultSubmit,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Find patient associated with current user
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=400, detail="Patient profile not found")
    session = save_game_result(db, patient.id, data)
    return {"message": "Result saved", "session_id": session.id}
''',

    "backend/app/main.py": '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app import models  # noqa: F401
from app.api import auth, games

app = FastAPI(title="Cognitive Gaming API")

# Allow frontend to call backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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

@app.get("/")
def read_root():
    return {"message": "Cognitive Gaming API is running"}
''',

    "frontend/src/services/api.js": '''const API_BASE_URL = 'http://localhost:8000';

export const api = {
  async login(email, password) {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });
    if (!res.ok) throw new Error('Login failed');
    return res.json();
  },
  async getMe(token) {
    const res = await fetch(`${API_BASE_URL}/api/auth/me`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('Not authenticated');
    return res.json();
  },
  async submitGameResult(token, resultData) {
    const res = await fetch(`${API_BASE_URL}/api/games/submit_result`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(resultData),
    });
    if (!res.ok) throw new Error('Failed to submit result');
    return res.json();
  }
};
''',

    "frontend/src/hooks/useGameSession.js": '''import { useState, useRef, useCallback } from 'react';
import { api } from '../services/api';

const useGameSession = (gameId, initialDifficulty = 'easy') => {
  const [difficulty, setDifficulty] = useState(initialDifficulty);
  const [score, setScore] = useState(0);
  const [attempts, setAttempts] = useState(0);
  const [mistakes, setMistakes] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [sessionStartTime, setSessionStartTime] = useState(null);
  const resultsRef = useRef([]);

  const startGame = useCallback(() => {
    setScore(0);
    setAttempts(0);
    setMistakes(0);
    resultsRef.current = [];
    setSessionStartTime(Date.now());
    setIsActive(true);
  }, []);

  const recordAnswer = useCallback((question, correctAnswer, userAnswer, isCorrect, reactionTimeMs) => {
    setAttempts(prev => prev + 1);
    if (!isCorrect) setMistakes(prev => prev + 1);
    if (isCorrect) setScore(prev => prev + 1);
    resultsRef.current.push({
      question,
      correct_answer: correctAnswer,
      user_answer: userAnswer,
      is_correct: isCorrect ? 1 : 0,
      reaction_time_ms: reactionTimeMs,
    });
  }, []);

  const endGame = useCallback(async () => {
    if (!isActive) return;
    const endTime = Date.now();
    const timeTaken = (endTime - sessionStartTime) / 1000;
    setIsActive(false);
    const accuracy = attempts > 0 ? (attempts - mistakes) / attempts : 0;
    const resultData = {
      game_id: gameId,
      score,
      accuracy,
      time_taken_seconds: timeTaken,
      mistakes,
      attempts,
      difficulty_level: difficulty,
      results: resultsRef.current,
    };
    try {
      const token = localStorage.getItem('token');
      if (!token) throw new Error('No token');
      await api.submitGameResult(token, resultData);
      console.log('Result submitted successfully');
    } catch (error) {
      console.error('Failed to submit result:', error);
    }
  }, [isActive, sessionStartTime, attempts, mistakes, score, gameId, difficulty]);

  return {
    difficulty,
    setDifficulty,
    score,
    attempts,
    mistakes,
    isActive,
    startGame,
    recordAnswer,
    endGame,
  };
};

export default useGameSession;
''',

    "frontend/src/pages/GameSelection.jsx": '''import { useState } from 'react';
import useGameSession from '../hooks/useGameSession';

function GameSelection({ onBack }) {
  const [selectedGame, setSelectedGame] = useState(null);
  const gameSession = useGameSession(1, 'easy'); // assume game_id=1 for Memory Game

  const games = [
    { id: 1, name: 'Memory Game', emoji: '🧠', description: 'Remember the objects' },
    { id: 2, name: 'Sequence Game', emoji: '🔢', description: 'Remember the order' },
    { id: 3, name: 'Attention Game', emoji: '🎯', description: 'Find the target' },
    { id: 4, name: 'Pattern Game', emoji: '🔷', description: 'Complete the pattern' },
  ];

  const startDemoGame = () => {
    setSelectedGame('memory');
    gameSession.startGame();
    // Simulate a few answers
    setTimeout(() => {
      gameSession.recordAnswer('Apple', 'Apple', 'Apple', true, 1000);
    }, 500);
    setTimeout(() => {
      gameSession.recordAnswer('House', 'House', 'Car', false, 1500);
    }, 1000);
    setTimeout(() => {
      gameSession.recordAnswer('Flower', 'Flower', 'Flower', true, 1200);
    }, 1500);
    setTimeout(() => {
      gameSession.endGame();
    }, 2000);
  };

  if (selectedGame === 'memory') {
    return (
      <div className="min-h-screen bg-gray-100 p-8">
        <button
          onClick={() => { setSelectedGame(null); }}
          className="mb-6 bg-gray-200 hover:bg-gray-300 text-xl px-4 py-2 rounded-lg"
        >
          ← Back
        </button>
        <h1 className="text-4xl font-bold text-blue-800 mb-8">Memory Game Demo</h1>
        <div className="bg-white p-6 rounded-2xl shadow-lg max-w-md">
          <p className="text-2xl mb-4">Status: {gameSession.isActive ? 'Playing...' : 'Finished'}</p>
          <p className="text-2xl mb-4">Score: {gameSession.score}</p>
          <p className="text-2xl mb-4">Attempts: {gameSession.attempts}</p>
          <p className="text-2xl mb-4">Mistakes: {gameSession.mistakes}</p>
          <button
            onClick={startDemoGame}
            className="w-full bg-green-500 hover:bg-green-600 text-white text-2xl font-bold py-4 rounded-xl"
            disabled={gameSession.isActive}
          >
            Start Demo Game
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <button
        onClick={onBack}
        className="mb-6 bg-gray-200 hover:bg-gray-300 text-xl px-4 py-2 rounded-lg"
      >
        ← Back
      </button>
      <h1 className="text-4xl font-bold text-blue-800 mb-8">Choose a Game</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {games.map((game) => (
          <button
            key={game.id}
            className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition text-center"
            onClick={() => {
              if (game.id === 1) startDemoGame();
              else alert(`${game.name} coming soon!`);
            }}
          >
            <span className="text-6xl">{game.emoji}</span>
            <p className="text-3xl font-semibold mt-4 text-gray-800">{game.name}</p>
            <p className="text-xl text-gray-500 mt-2">{game.description}</p>
          </button>
        ))}
      </div>
    </div>
  );
}

export default GameSelection;
'''
}

for filename, content in files.items():
    filepath = Path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content.strip(), encoding='utf-8')
    print(f"Written {filepath}")

print("\nPhase 5 files created successfully!")
