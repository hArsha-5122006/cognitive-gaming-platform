from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.caregiver import Caregiver
from app.models.patient import Patient
from app.services.caregiver_service import get_caregiver_dashboard
from app.services.alert_service import generate_caregiver_alerts

router = APIRouter()

class LinkPatientRequest(BaseModel):
    patient_email: str

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

@router.post("/link")
def link_patient(
    data: LinkPatientRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != 'caregiver' and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    # Find caregiver profile
    caregiver = db.query(Caregiver).filter(Caregiver.user_id == current_user.id).first()
    if not caregiver:
        raise HTTPException(status_code=400, detail="Caregiver profile not found")
    # Find patient by email
    patient = db.query(Patient).join(Patient.user).filter(Patient.user.has(email=data.patient_email)).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient with this email not found")
    # Check if already linked
    if patient in caregiver.patients:
        return {"message": "Patient already linked"}
    caregiver.patients.append(patient)
    db.commit()
    return {"message": "Patient linked successfully", "patient_id": patient.id}
