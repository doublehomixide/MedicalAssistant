from datetime import datetime
import sqlalchemy
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from backend.CreateReadUpdateDelete.utilities import clean_call_of_error
from backend.SchemasNModels.models.models import AppointmentModel, UserModel
from backend.SchemasNModels.schemas.user_n_appointments_schemas import UserInDB


class AppointmentCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def create_appointment(self, time: datetime,
                                 unique_id: str,
                                 customer: UserInDB,
                                 doctor_name: str,
                                 ):
        db_model = AppointmentModel(
            user_username=customer.username,
            doctor_username=doctor_name,
            time=time,
            unique_id=unique_id
        )
        try:
            self.db_session.add(db_model)
            return db_model
        except sqlalchemy.exc.IntegrityError as error:
            error_message = str(error.orig)
            clean_call_of_error(error_message)

    async def read_appointments(self, username: str):
        statement = select(AppointmentModel).where(AppointmentModel.user_username == username)
        request = await self.db_session.execute(statement)
        result = request.scalars().all()
        return result

    async def delete_appointment(self, number_of_appointment: str, user: UserInDB):
        statement = delete(AppointmentModel).where(
            (AppointmentModel.user_username == user.username) & (AppointmentModel.unique_id == number_of_appointment))
        request = await self.db_session.execute(statement)
        return {'status': 'success',
                f'appointment №{number_of_appointment}': 'deleted'}
