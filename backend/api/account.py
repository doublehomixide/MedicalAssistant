from backend.CreateReadUpdateDelete.user import UserCRUD
from fastapi import APIRouter, Depends
from backend.CreateReadUpdateDelete.depends import get_user_crud
from backend.SchemasNModels.schemas.choose_one import Options
from backend.SchemasNModels.schemas.user_n_appointments_schemas import UserInDB
from backend.authentication.action.user import get_current_user

router = APIRouter(prefix='/user', tags=['Управление учетной записью'])


@router.get('/info', description='Обо мне')
async def info_about_me(user: UserInDB = Depends(get_current_user)):
    return user


@router.put('/update/{type_of_data}', description='Обновить данные учетной записи')
async def update_user(type_of_data: Options, data: str,
                      user: UserInDB = Depends(get_current_user),
                      db: UserCRUD = Depends(get_user_crud)) -> dict:
    return await db.update_current_user_data(type_of_data=type_of_data, data=data, user=user)


@router.delete("/delete", description='Удалить учетную запись')
async def delete_user(
        user: UserInDB = Depends(get_current_user),
        db: UserCRUD = Depends(get_user_crud)
):
    return await db.delete_user(user)
