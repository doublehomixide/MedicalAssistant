from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from backend.CreateReadUpdateDelete.depends import get_user_crud
from backend.CreateReadUpdateDelete.user import UserCRUD
from backend.SchemasNModels.schemas import user_n_appointments_schemas as schemas
from backend.SchemasNModels.schemas.user_n_appointments_schemas import UserRegistration
from backend.authentication.action.user import validate_user
from backend.authentication.utilities import create_access_token, create_refresh_token

router = APIRouter(tags=['Учетная запись'])


@router.post('/register')
async def register_new_user(
        user: Annotated[schemas.UserRegistration, Depends()],
        db: UserCRUD = Depends(get_user_crud)
) -> UserRegistration:
    return await db.create_user(user)

