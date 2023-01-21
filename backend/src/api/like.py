import datetime

from fastapi import APIRouter, Depends

from src import models
from src.pydantic_models.like import CreateLike, DeleteLike
from src.pydantic_models.user import User
from src.services.auth import get_current_user
from src.services.like import LikeService

router = APIRouter(
    prefix='/like'
)


@router.post('/create', response_model=User)
async def create_new_like(
        like_data: CreateLike,
        user: models.User = Depends(get_current_user),
        service: LikeService = Depends()
):
    return await service.create_new_like(like_data, user.id)


@router.delete('/delete')
async def delete_like(
        like_data: DeleteLike,
        user: models.User = Depends(get_current_user),
        service: LikeService = Depends()
):
    return await service.delete_like(like_data, user.id)


@router.get('/get-statistic')
async def get_amount_of_likes_during_period(
        start_date: datetime.date,
        end_date: datetime.date,
        service: LikeService = Depends()
):
    return await service.get_statistic_for_period(start_date, end_date)
