from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True))
    status = Column(String, default="in_progress")  # 'in_progress', 'completed', 'abandoned'
    score = Column(Float)
    accuracy = Column(Float)
    time_taken_seconds = Column(Float)
    mistakes = Column(Integer)
    attempts = Column(Integer)
    difficulty_level = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="game_sessions")
    game = relationship("Game")
    results = relationship("GameResult", back_populates="session")
