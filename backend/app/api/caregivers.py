from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.auth import get_current_user
from app.services.caregiver_service import get_caregiver_dashboard
from app.services.alert_service import generate_caregiver_alerts

router = APIRouter()

@router.get("/dashboard")
def caregiver_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != 'caregiver' and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    data = get_caregiver_dashboard(db, current_user.id)
    return data

@router.get("/alerts/{patient_id}")
def get_patient_alerts(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != 'caregiver' and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    alerts = generate_caregiver_alerts(db, patient_id)
    return alerts
