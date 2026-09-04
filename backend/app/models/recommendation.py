from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"))
    difficulty_level = Column(String)
    reason = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient")
    game = relationship("Game")
