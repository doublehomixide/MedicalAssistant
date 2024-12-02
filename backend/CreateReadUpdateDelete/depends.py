from typing import Generator

from backend.CreateReadUpdateDelete.appointment import AppointmentCRUD
from backend.CreateReadUpdateDelete.object_crud import DoctorCRUD
from backend.database.database_config import async_session
from backend.CreateReadUpdateDelete.object_crud import UserCRUD


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


async def get_doctor_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield DoctorCRUD(session)
