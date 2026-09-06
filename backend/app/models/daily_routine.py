from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class DailyRoutineItem(Base):
    __tablename__ = "daily_routine_items"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    title = Column(String, nullable=False)
    scheduled_time = Column(String, nullable=False)  # e.g., "7:00 AM"
    is_completed = Column(Boolean, default=False)
    completed_date = Column(Date)  # stores the date when marked completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
