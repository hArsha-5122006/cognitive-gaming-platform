from pydantic import BaseModel
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