from typing import Annotated

from fastapi import APIRouter, Depends

from backend.CreateReadUpdateDelete.depends import get_doctor_crud
from backend.CreateReadUpdateDelete.object_crud import DoctorCRUD
from backend.SchemasNModels.schemas.user_n_appointments_schemas import DoctorRegistration

router = APIRouter(prefix='/authentication', tags=['Управление учетной записью врача'])


@router.post('/new_doctor')
async def register_new_doctor(
        doctor: Annotated[DoctorRegistration, Depends()],
        db: DoctorCRUD = Depends(get_doctor_crud)
):
    return await db.create_object(doctor)
