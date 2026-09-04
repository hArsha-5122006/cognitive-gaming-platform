from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.database import Base

caregiver_patient_association = Table(
    'caregiver_patient_association',
    Base.metadata,
    Column('caregiver_id', Integer, ForeignKey('caregivers.id')),
    Column('patient_id', Integer, ForeignKey('patients.id'))
)
