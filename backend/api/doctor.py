from typing import Annotated

from fastapi import APIRouter, Depends

from backend.CreateReadUpdateDelete.depends import get_doctor_crud
from backend.CreateReadUpdateDelete.doctor import DoctorCRUD
from backend.SchemasNModels.schemas.user_n_appointments_schemas import DoctorRegistration, UserRegistration
from backend.authentication.action.user import get_current_user

router = APIRouter(prefix='/authentication', tags=['Управление учетной записью врача'])


@router.post('/new_doctor')
async def register_new_doctor(
        doctor: Annotated[DoctorRegistration, Depends()],
        db: DoctorCRUD = Depends(get_doctor_crud)
):
    return await db.create_doctor(doctor)


@router.get('/all_doctors')
async def get_doctors(user: UserRegistration = Depends(get_current_user),
                      db: DoctorCRUD = Depends(get_doctor_crud)):
    return await db.read_doctors()
