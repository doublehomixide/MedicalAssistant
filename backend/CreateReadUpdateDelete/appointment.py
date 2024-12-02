import re
from datetime import datetime

import sqlalchemy
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.SchemasNModels.models.models import AppointmentModel, UserModel
from backend.SchemasNModels.schemas.user_n_appointments_schemas import User, Doctor, DoctorRegistration


class AppointmentCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def create_appointment(self, full_customer: User,
                                 doctor_name: str,
                                 time: datetime,
                                 unique_id: str):
        statement = select(DoctorRegistration).where(DoctorRegistration.displayed_name == doctor_name)
        request = await self.db_session.execute(statement)
        full_doctor = request.scalars().all()

        customer = User(**full_customer)
        doctor = Doctor(**full_doctor)
        db_model = AppointmentModel(
            Customer=customer,
            Doctor=doctor,
            time=time,
            unique_id=unique_id
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

    async def read_appointments(self, username: str):
        statement = select(AppointmentModel).where(AppointmentModel.Customer.username == username)
        request = await self.db_session.execute(statement)
        result = request.scalars().all()
        return result
