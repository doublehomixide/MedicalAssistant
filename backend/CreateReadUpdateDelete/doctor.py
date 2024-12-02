import re
from typing import List

import sqlalchemy
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.SchemasNModels.models.models import DoctorModel
from backend.SchemasNModels.schemas.user_n_appointments_schemas import DoctorRegistration
from backend.authentication.utilities import get_password_hash


class DoctorCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def create_doctor(self,
                            doctor: DoctorRegistration):
        db_model = DoctorModel(
            username=doctor.username,
            displayed_name=doctor.displayed_name,
            email=doctor.email,
            telephone_number=doctor.telephone_number,
            hashed_password=get_password_hash(doctor.password),
            specialization=doctor.specialization,
            photo=doctor.photo
        )
        try:
            self.db_session.add(db_model)
            return db_model
        except sqlalchemy.exc.IntegrityError as error:
            error_message = str(error.orig)
            if error_message:
                error_message_step1 = re.search(r'Ключ \"\((.*?)\)\" уже существует', error_message)
                error_message_step2 = error_message_step1.group(1)
                clear_error_message = error_message_step2.split(')=(')
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{clear_error_message[0]} {clear_error_message[1]} already exist"
                )

    async def read_doctors(self) -> List[DoctorModel]:
        statement = select(DoctorModel)
        request = await self.db_session.execute(statement)
        result = request.scalars().all()
        return result

    async def read_doctor_by_user_name(self, username: str):
        statement = select(DoctorModel).where(DoctorModel.username == username)
        request = await self.db_session.execute(statement)
        result = request.scalars().first()
        return result
