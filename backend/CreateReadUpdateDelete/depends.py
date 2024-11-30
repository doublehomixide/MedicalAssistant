from typing import Generator

from backend.database.database_config import async_session
from backend.CreateReadUpdateDelete.user import UserCRUD


async def get_db() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield session


async def get_user_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield UserCRUD(session)


# async def get_appointment_crud() -> Generator:
#     async with async_session() as session:
#         async with session.begin():
#             yield AppointmentCRUD(session)