from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class DailyRoutineCreate(BaseModel):
    title: str
    scheduled_time: str  # e.g., "7:00 AM"

class DailyRoutineUpdate(BaseModel):
    is_completed: bool

class DailyRoutineOut(BaseModel):
    id: int
    patient_id: int
    title: str
    scheduled_time: str
    is_completed: bool
    completed_date: Optional[date]
    created_at: datetime

    class Config:
        from_attributes = True
