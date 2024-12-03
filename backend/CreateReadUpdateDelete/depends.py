from typing import Generator
from fastapi import HTTPException, Depends
from starlette import status
from backend.SchemasNModels.schemas.user_n_appointments_schemas import UserInDB
from backend.authentication.action.user import get_current_user
from backend.database.database_config import async_session
from backend.CreateReadUpdateDelete.user import UserCRUD
from backend.CreateReadUpdateDelete.appointment import AppointmentCRUD


async def get_db() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield session


async def get_user_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield UserCRUD(session)


async def get_appointment_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield AppointmentCRUD(session)


class PermissionChecker:

    def __init__(self, required_role: str) -> None:
        self.required_role = required_role

    def __call__(self, user: UserInDB = Depends(get_current_user)) -> bool:
        for r_role in self.required_role:
            if r_role not in user.role:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Permissions'
                )
        return True
