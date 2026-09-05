from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReminderCreate(BaseModel):
    title: str
    description: Optional[str] = None
    reminder_type: str  # 'medicine', 'hydration', 'activity', 'appointment'
    scheduled_time: datetime

class ReminderUpdate(BaseModel):
    is_completed: bool

class ReminderOut(BaseModel):
    id: int
    patient_id: int
    title: str
    description: Optional[str]
    reminder_type: str
    scheduled_time: datetime
    is_completed: bool
    completed_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
