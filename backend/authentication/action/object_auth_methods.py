from fastapi import Depends, HTTPException
from jose import jwt
from typing import Annotated

from backend.database.database_config import async_session
from backend.CreateReadUpdateDelete.object_crud import UserCRUD, DoctorCRUD
from backend.authentication.utilities import verify_password, oauth2_scheme_users, oauth2_scheme_doctors
from config import get_settings

settings = get_settings()


class ObjectAuthMethods:
    oauth_scheme = None  # заменить на нужную oauth scheme
    CRUD = None

    async def validate_object(self, username: str, password: str):
        async with async_session() as session:
            async with session.begin():
                db = self.CRUD(session)
                user = await db.read_object_by_username(username=username)
                if not user:
                    return False

                if not verify_password(password, user.hashed_password):
                    return False
                return user

    async def get_current_object(self, token: Annotated[str, Depends(oauth_scheme)]):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )
            username: str = payload.get("username")
            if username is None:
                raise credentials_exception

        except Exception as e:
            credentials_exception.detail = str(e)
            raise credentials_exception

        async with async_session() as session:
            async with session.begin():
                db = self.CRUD(session)
                objectt = await db.read_object_by_username(username=username)
                if objectt is None:
                    raise credentials_exception
                return objectt


class UserAuthMethods(ObjectAuthMethods):
    oauth_scheme = oauth2_scheme_users
    CRUD = UserCRUD


class DoctorAuthMethods(ObjectAuthMethods):
    oauth_scheme = oauth2_scheme_doctors
    CRUD = DoctorCRUD
