from datetime import datetime
from typing import Annotated, Literal
from fastapi import APIRouter, Depends
from backend.CreateReadUpdateDelete.appointment import AppointmentCRUD
from backend.CreateReadUpdateDelete.depends import get_appointment_crud, PermissionChecker
from backend.SchemasNModels.schemas.user_n_appointments_schemas import UserInDB
from backend.authentication.action.user import get_current_user

router = APIRouter(prefix='/appointment', tags=['Управление записями'])


@router.post('/new_appointment', description='Записаться к врачу')
async def create_appointment(time: datetime,
                             unique_id: str,
                             doctor_name: Literal['testingdoctor', 'gandon'],
                             customer: UserInDB = Depends(get_current_user),
                             db: AppointmentCRUD = Depends(get_appointment_crud),
                             is_authorized: bool = Depends(PermissionChecker('doctor'))):
    return await db.create_appointment(time, unique_id, customer, doctor_name)


@router.get('/my_appointments', description='Мои записи')
async def my_appointments(customer: UserInDB = Depends(get_current_user),
                          db: AppointmentCRUD = Depends(get_appointment_crud)):
    return await db.read_appointments(customer.username)


@router.delete('/delete_appointment', description='Удалить запись')
async def delete_appointment(number_of_appointment: str,
                             customer: UserInDB = Depends(get_current_user),
                             db: AppointmentCRUD = Depends(get_appointment_crud)):
    return await db.delete_appointment(number_of_appointment, customer)
