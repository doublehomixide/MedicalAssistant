from datetime import datetime
import sqlalchemy.exc
from fastapi import Depends, HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
import re
from backend.SchemasNModels.models import models
from backend.SchemasNModels.models.models import UserModel
from backend.SchemasNModels.schemas import user_n_appointments_schemas as schemas
from backend.SchemasNModels.schemas.user_n_appointments_schemas import UserRegistration
from backend.authentication.utilities import get_password_hash


class UserCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def create_user(self, user: schemas.UserRegistration) -> schemas.UserRegistration:
        db_model = models.UserModel(
            username=user.username,
            displayed_name=user.displayed_name,
            email=user.email,
            telephone_number=user.email,
            hashed_password=get_password_hash(user.password)
        )
        try:
            self.db_session.add(db_model)
            await self.db_session.commit()
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

    async def read_user_by_username(self, username: str) -> UserRegistration:
        statement = select(UserModel).where(UserModel.username == username)
        request = await self.db_session.execute(statement)
        result = request.scalars().first()
        return result

    async def update_current_user_data(self, type_of_data: str, data: str, user: UserRegistration) -> dict:
        username = user.username
        statement = update(UserModel).where(UserModel.username == username).values(**{type_of_data: data})
        statement.execution_options(synchronize_session="fetch")
        await self.db_session.execute(statement)
        return {'status': 'Данные успешно обновлены'}

    async def update_user_login(self, username: str):
        db_user = await self.read_user_by_username(username)
        db_user.last_login = datetime.utcnow()
        await self.db_session.refresh(db_user)
        return db_user

    async def delete_user(self, user: UserRegistration):
        username = user.username
        statement = delete(UserModel).where(UserModel.username == username)
        statement.execution_options(synchronize_session='fetch')
        await self.db_session.execute(statement)
        return {"status":"success",
                username:"deleted"}
