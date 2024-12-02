import re
from datetime import datetime

import sqlalchemy
from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.SchemasNModels.models.models import UserModel, DoctorModel
from backend.SchemasNModels.schemas.user_n_appointments_schemas import UserRegistration, DoctorRegistration


def get_clear_data_of_error(error_message):
    if error_message:
        error_message_step1 = re.search(r'Ключ \"\((.*?)\)\" уже существует', error_message)
        error_message_step2 = error_message_step1.group(1)
        clear_error_message = error_message_step2.split(')=(')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{clear_error_message[0]} {clear_error_message[1]} already exist"
        )


class ObjectCRUD:
    db_session = None
    model_of_crud = None  # заменить на модель
    schema_of_crud = None  # на его схему регистрации

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def create_object(self, schema_object: schema_of_crud) -> schema_of_crud:
        db_model = (schema_object.model_dump())
        try:
            self.db_session.add(db_model)
            return db_model
        except sqlalchemy.exc.IntegrityError as error:
            error_message = str(error.orig)
            get_clear_data_of_error(error_message)

    async def read_object_by_username(self, username: str) -> schema_of_crud:
        statement = select(self.model_of_crud).where(self.model_of_crud.username == username)
        request = await self.db_session.execute(statement)
        result = request.scalars().first()
        return result

    async def update_current_object_data(self, type_of_data: str, data: str,
                                         user: UserRegistration) -> dict:
        username = user.username
        statement = update(self.model_of_crud).where(self.model_of_crud.username == username) \
            .values(**{type_of_data: data})
        statement.execution_options(synchronize_session="fetch")
        await self.db_session.execute(statement)
        return {'status': 'Данные успешно обновлены'}

    async def update_object_login(self, username: str):
        db_user = await self.read_object_by_username(username)
        db_user.last_login = datetime.utcnow()
        await self.db_session.refresh(db_user)
        return db_user

    async def delete_object(self, user: UserRegistration):
        username = user.username
        statement = delete(self.model_of_crud).where(self.model_of_crud.username == username)
        statement.execution_options(synchronize_session='fetch')
        await self.db_session.execute(statement)
        return {"status": "success",
                username: "deleted"}


class UserCRUD(ObjectCRUD):
    model_of_crud = UserModel
    schema_of_crud = UserRegistration


class DoctorCRUD(ObjectCRUD):
    model_of_crud = DoctorModel
    schema_of_crud = DoctorRegistration
