from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm

from src import models
from src.pydantic_models.jwt_token import Token
from src.pydantic_models.user import CreateUser, User, UserStatistic
from src.services.auth import AuthService, get_current_user
from src.services.user import UserService

router = APIRouter(
    prefix='/auth'
)


@router.post('/sign-up', response_model=Token)
async def create_new_user(
        user_data: CreateUser,
        service: AuthService = Depends(),
):
    return await service.create_new_user(user_data)


@router.post('/sign-in', response_model=Token)
async def authenticate_user(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(),
):
    return await service.authenticate_user(user_credentials.username, user_credentials.password)


@router.get('/user', response_model=User)
async def get_user(
        user: models.User = Depends(get_current_user)
):
    return user


@router.get('/get-statistic', response_model=UserStatistic)
async def get_user_statistic(
        user: models.User = Depends(get_current_user),
        service: UserService = Depends()
):
    return await service.get_user_statistic(user.id)
