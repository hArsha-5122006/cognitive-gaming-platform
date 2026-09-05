from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.patient import Patient
from app.models.caregiver import Caregiver

def get_patient_if_authorized(patient_id: int, current_user, db: Session):
    """
    Check if the current user can access the given patient's data.
    - If user is the patient themselves (via patient.user_id), allow.
    - If user is a caregiver linked to this patient, allow.
    - If user is admin, allow.
    Otherwise, raise 403.
    """
    if current_user.role == 'admin':
        return db.query(Patient).filter(Patient.id == patient_id).first()

    if current_user.role == 'patient':
        patient = db.query(Patient).filter(
            Patient.id == patient_id,
            Patient.user_id == current_user.id
        ).first()
        if patient:
            return patient
        raise HTTPException(status_code=403, detail="Not authorized to access this patient's data")

    if current_user.role == 'caregiver':
        caregiver = db.query(Caregiver).filter(Caregiver.user_id == current_user.id).first()
        if not caregiver:
            raise HTTPException(status_code=403, detail="Caregiver profile not found")
        # Check if caregiver is linked to the patient
        linked = db.query(Patient).join(
            "caregivers"  # using the relationship name defined in Patient model
        ).filter(Patient.id == patient_id, Caregiver.id == caregiver.id).first()
        if linked:
            return linked
        raise HTTPException(status_code=403, detail="Not authorized to access this patient's data")

    raise HTTPException(status_code=403, detail="Not authorized")
