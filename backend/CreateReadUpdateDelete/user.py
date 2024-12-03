import sqlalchemy.exc
from fastapi import Depends, HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
import re

from backend.CreateReadUpdateDelete.utilities import clean_call_of_error
from backend.SchemasNModels.models import models
from backend.SchemasNModels.models.models import UserModel
from backend.SchemasNModels.schemas.user_n_appointments_schemas import UserInput, UserInDB
from backend.authentication.utilities import get_password_hash


class UserCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def create_user(self, user: UserInDB) -> UserInDB:
        db_model = models.UserModel(
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            telephone_number=user.email,
            password=get_password_hash(user.password),
            role=user.role
        )
        try:
            self.db_session.add(db_model)
            return db_model
        except sqlalchemy.exc.IntegrityError as error:
            error_message = str(error.orig)
            clean_call_of_error(error_message)

    async def read_user_by_username(self, username: str) -> UserInDB:
        statement = select(UserModel).where(UserModel.username == username)
        request = await self.db_session.execute(statement)
        result = request.scalars().first()
        return result

    async def update_current_user_data(self, type_of_data: str, data: str, user: UserInput) -> dict:
        username = user.username
        statement = update(UserModel).where(UserModel.username == username).values(**{type_of_data: data})
        statement.execution_options(synchronize_session="fetch")
        await self.db_session.execute(statement)
        return {'status': 'Данные успешно обновлены'}

    async def delete_user(self, user: UserInDB):
        username = user.username
        statement = delete(UserModel).where(UserModel.username == username)
        statement.execution_options(synchronize_session='fetch')
        await self.db_session.execute(statement)
        return {"status": "success",
                username: "deleted"}
