from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class CognitiveScore(Base):
    __tablename__ = "cognitive_scores"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"))
    score_type = Column(String)  # 'memory', 'attention', 'reaction', 'pattern', 'overall'
    score_value = Column(Float)
    session_id = Column(Integer, ForeignKey("game_sessions.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="cognitive_scores")
    game = relationship("Game")
    session = relationship("GameSession")
