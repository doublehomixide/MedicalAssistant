from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from starlette import status

from backend.CreateReadUpdateDelete.depends import get_doctor_crud
from backend.CreateReadUpdateDelete.object_crud import DoctorCRUD
from backend.SchemasNModels.schemas import user_n_appointments_schemas as schemas
from backend.SchemasNModels.schemas.token import Token
from backend.authentication.action.object_auth_methods import DoctorAuthMethods
from backend.authentication.utilities import create_access_token, create_refresh_token
from config import get_settings

router = APIRouter(prefix='/doctor_authentication',tags=['Аутенфикация мед персонала'])
settings = get_settings()


@router.post('/register')
async def register_new_user(
        user: Annotated[schemas.UserRegistration, Depends()],
        db: DoctorCRUD = Depends(get_doctor_crud)
):
    return await db.create_object(user)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logout successfully"}


@router.post("/login", response_model=Token)
async def login(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: DoctorCRUD = Depends(get_doctor_crud),
):
    user = await DoctorAuthMethods.validate_object(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await create_access_token(data={"username": form_data.username})
    refresh_token = await create_refresh_token(data={"username": form_data.username})

    await db.update_object_login(username=form_data.username)
    expired_time = (
            int(datetime.now(tz=timezone.utc).timestamp() * 1000)
            + timedelta(minutes=settings.ACCESS_TOKEN_TIME).seconds * 1000
    )

    response.set_cookie(
        access_token,
        refresh_token,
        httponly=True,
        samesite="strict",
        secure=False,
        expires=timedelta(settings.REFRESH_TOKEN_DAYS),
    )

    return Token(
        access_token=access_token,
        expires_in=expired_time,
        token_type="Bearer",
    )


@router.post("/refresh", response_model=Token)
async def refresh(
        request: Request,
        response: Response,
        db: DoctorCRUD = Depends(get_doctor_crud),
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise credentials_exception

        payload = jwt.decode(
            refresh_token,
            settings.refresh_token_secret,
            algorithms=["HS256"],
        )

        username: str = payload.get("username")
        if username is None:
            raise credentials_exception

    except Exception as e:
        credentials_exception.detail = str(e)
        raise credentials_exception

    access_token = await create_access_token(data={"sub": username})
    refresh_token = await create_refresh_token(data={"sub": username})

    await db.update_object_login(username=username)
    expired_time = (
            int(datetime.now(tz=timezone.utc).timestamp() * 1000)
            + timedelta(minutes=settings.access_token_expire_minutes).seconds * 1000
    )

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        samesite="strict",
        secure=False,
        expires=timedelta(settings.refresh_token_expire_minutes),
    )

    return Token(
        access_token=access_token,
        expires_in=expired_time,
        token_type="Bearer",
    )
