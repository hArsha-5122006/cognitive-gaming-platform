from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.auth import get_current_user
from app.core.permissions import get_patient_if_authorized
from app.models.patient import Patient
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderOut

router = APIRouter()

def get_patient_for_current_user(db: Session, user):
    patient = db.query(Patient).filter(Patient.user_id == user.id).first()
    if not patient:
        raise HTTPException(status_code=400, detail="Patient profile not found")
    return patient

@router.get("/", response_model=List[ReminderOut])
def get_reminders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    patient = get_patient_for_current_user(db, current_user)
    reminders = db.query(Reminder).filter(Reminder.patient_id == patient.id).order_by(Reminder.scheduled_time).all()
    return reminders

@router.post("/", response_model=ReminderOut, status_code=status.HTTP_201_CREATED)
def create_reminder(
    data: ReminderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    patient = get_patient_for_current_user(db, current_user)
    reminder = Reminder(
        patient_id=patient.id,
        title=data.title,
        description=data.description,
        reminder_type=data.reminder_type,
        scheduled_time=data.scheduled_time
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

@router.patch("/{reminder_id}/complete", response_model=ReminderOut)
def complete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    patient = get_patient_for_current_user(db, current_user)
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.patient_id == patient.id
    ).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    reminder.is_completed = True
    from datetime import datetime
    reminder.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(reminder)
    return reminder
