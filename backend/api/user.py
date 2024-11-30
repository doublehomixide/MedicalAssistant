from typing import Annotated

from backend.CreateReadUpdateDelete.user import UserCRUD
from backend.SchemasNModels.schemas import user_n_appointments_schemas as schemas
from fastapi import APIRouter, Depends
from backend.CreateReadUpdateDelete.depends import get_user_crud
from backend.SchemasNModels.schemas.choose_one import Options
from backend.SchemasNModels.schemas.user_n_appointments_schemas import UserRegistration
from backend.authentication.action.user import get_current_user

router = APIRouter(prefix='/user', tags=['Учетная запись'])



@router.get('/me_info')
async def info_about_me(user: schemas.UserRegistration = Depends(get_current_user)) -> UserRegistration:
    return user


@router.put('/update/{type_of_data}')
async def update_user(type_of_data: Options, data: str,
                      user: schemas.UserRegistration = Depends(get_current_user),
                      db: UserCRUD = Depends(get_user_crud)) -> dict:
    return await db.update_current_user_data(type_of_data=type_of_data, data=data, user=user)
