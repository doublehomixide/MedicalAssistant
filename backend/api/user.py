from backend.CreateReadUpdateDelete.object_crud import UserCRUD
from backend.SchemasNModels.schemas import user_n_appointments_schemas as schemas
from fastapi import APIRouter, Depends
from backend.CreateReadUpdateDelete.depends import get_user_crud
from backend.SchemasNModels.schemas.choose_one import Options
from backend.SchemasNModels.schemas.user_n_appointments_schemas import UserRegistration
from backend.authentication.action.object_auth_methods import UserAuthMethods

router = APIRouter(prefix='/user', tags=['Управление учетной записью'])


@router.get('/info')
async def info_about_me(user: UserRegistration = Depends(UserAuthMethods.get_current_object)):
    return user


@router.put('/update/{type_of_data}')
async def update_user(type_of_data: Options, data: str,
                      user: UserRegistration = Depends(UserAuthMethods.get_current_object),
                      db: UserCRUD = Depends(get_user_crud)) -> dict:
    return await db.update_current_object_data(type_of_data=type_of_data, data=data, user=user)


@router.delete("/delete")
async def delete_user(
        user: schemas.UserRegistration = Depends(UserAuthMethods.get_current_object),
        db: UserCRUD = Depends(get_user_crud)
):
    return await db.delete_object(user)
