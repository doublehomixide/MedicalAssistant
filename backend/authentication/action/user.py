from fastapi import Depends, HTTPException
from jose import jwt
from typing import Annotated

from backend.database.database_config import async_session
from backend.CreateReadUpdateDelete.user import UserCRUD
from backend.authentication.utilities import verify_password, oauth2_scheme
from config import get_settings

settings = get_settings()

async def validate_user(username: str, password: str):
    async with async_session() as session:
        async with session.begin():
            db = UserCRUD(session)
            user = await db.read_user_by_username(username=username)
            if not user:
                return False

            if not verify_password(password, user.hashed_password):
                return False
            return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
            db = UserCRUD(session)
            user = await db.read_user_by_username(username=username)
            if user is None:
                raise credentials_exception
            return user
