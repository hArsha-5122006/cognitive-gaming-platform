from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.patient import Patient
from app.models.daily_routine import DailyRoutineItem
from app.schemas.daily_routine import DailyRoutineCreate, DailyRoutineUpdate, DailyRoutineOut

router = APIRouter()

def get_patient_for_current_user(db, user):
    patient = db.query(Patient).filter(Patient.user_id == user.id).first()
    if not patient:
        raise HTTPException(status_code=400, detail="Patient profile not found")
    return patient

@router.get("/", response_model=List[DailyRoutineOut])
def get_daily_routine(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    patient = get_patient_for_current_user(db, current_user)
    today = date.today()
    # Reset completion if completed_date is not today
    items = db.query(DailyRoutineItem).filter(DailyRoutineItem.patient_id == patient.id).all()
    for item in items:
        if item.completed_date != today:
            item.is_completed = False
            item.completed_date = None
    db.commit()
    # Fetch updated
    items = db.query(DailyRoutineItem).filter(DailyRoutineItem.patient_id == patient.id).all()
    return items

@router.post("/", response_model=DailyRoutineOut, status_code=201)
def create_daily_routine_item(
    data: DailyRoutineCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    patient = get_patient_for_current_user(db, current_user)
    item = DailyRoutineItem(
        patient_id=patient.id,
        title=data.title,
        scheduled_time=data.scheduled_time,
        is_completed=False
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.patch("/{item_id}/complete", response_model=DailyRoutineOut)
def complete_daily_routine_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    patient = get_patient_for_current_user(db, current_user)
    item = db.query(DailyRoutineItem).filter(
        DailyRoutineItem.id == item_id,
        DailyRoutineItem.patient_id == patient.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Routine item not found")
    today = date.today()
    # Toggle completion
    if item.completed_date == today:
        item.is_completed = False
        item.completed_date = None
    else:
        item.is_completed = True
        item.completed_date = today
    db.commit()
    db.refresh(item)
    return item
