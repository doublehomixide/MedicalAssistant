import datetime

from fastapi import APIRouter, Depends

from backend.CreateReadUpdateDelete.appointment import AppointmentCRUD
from backend.CreateReadUpdateDelete.depends import get_appointment_crud
from backend.SchemasNModels.schemas.user_n_appointments_schemas import UserRegistration, DoctorRegistration
from backend.authentication.action.user import get_current_user

router = APIRouter(prefix='/appointment', tags=['Управление записями к врачу'])


@router.post('/new_appointment')
async def create_appointment(doctor: str,
                          time: datetime.datetime,
                          unique_id: str,
                          customer: UserRegistration = Depends(get_current_user),
                          db: AppointmentCRUD = Depends(get_appointment_crud)):
    return await db.create_appointment(customer, doctor, time, unique_id)

@router.get('/my_appointments')
async def my_appointments(customer: UserRegistration=Depends(get_current_user),
                          db: AppointmentCRUD=Depends(get_appointment_crud)):
    return await db.read_appointments(customer.username)
