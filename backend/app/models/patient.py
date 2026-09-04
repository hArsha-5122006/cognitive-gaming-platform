from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_of_birth = Column(Date)
    gender = Column(String)
    language_preference = Column(String, default="English")
    address = Column(String)
    emergency_contact = Column(String)
    medical_notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", backref="patient")
    caregivers = relationship("Caregiver", secondary="caregiver_patient_association", back_populates="patients")
    game_sessions = relationship("GameSession", back_populates="patient")
    cognitive_scores = relationship("CognitiveScore", back_populates="patient")
    reminders = relationship("Reminder", back_populates="patient")
