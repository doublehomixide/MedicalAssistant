import datetime

from fastapi import APIRouter, Depends

from backend.CreateReadUpdateDelete.appointment import AppointmentCRUD
from backend.CreateReadUpdateDelete.depends import get_appointment_crud
from backend.SchemasNModels.schemas.user_n_appointments_schemas import UserRegistration
from backend.authentication.action.object_auth_methods import UserAuthMethods

router = APIRouter(prefix='/appointment', tags=['Управление записями к врачу'])


@router.post('/new_appointment')
async def create_appointment(doctor: str,
                             time: datetime.datetime,
                             unique_id: str,
                             customer: UserRegistration = Depends(UserAuthMethods.get_current_object),
                             db: AppointmentCRUD = Depends(get_appointment_crud)):
    return await db.create_appointment(customer, doctor, time, unique_id)


@router.get('/my_appointments')
async def my_appointments(customer: UserRegistration = Depends(UserAuthMethods.get_current_object),
                          db: AppointmentCRUD = Depends(get_appointment_crud)):
    return await db.read_appointments(customer.username)
