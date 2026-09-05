from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.auth import get_current_user
from app.services.caregiver_service import get_caregiver_dashboard

router = APIRouter()

@router.get("/dashboard")
def caregiver_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != 'caregiver' and current_user.role != 'admin':
        return {"error": "Not authorized"}
    data = get_caregiver_dashboard(db, current_user.id)
    return data
