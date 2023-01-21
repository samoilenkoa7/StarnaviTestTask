import datetime
import uuid

from fastapi import Depends, HTTPException, Response
from starlette import status

from src import models
from src.pydantic_models.like import CreateLike, DeleteLike

from src.services.likeDAL import LikeDAL


class LikeService:

    EXCEPTION = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail='Internal server error')

    def __init__(self, db_service: LikeDAL = Depends()):
        self.db_service = db_service

    async def create_new_like(self,
                              like_data: CreateLike,
                              user_id: uuid.UUID) -> models.PostLike:
        new_like = await self.db_service.create_like(user_id=user_id, post_id=like_data.post_id)
        if not new_like:
            raise self.EXCEPTION
        return new_like

    async def delete_like(self,
                          like_data: DeleteLike,
                          user_id: uuid.UUID) -> Response:
        await self.db_service.delete_like(user_id=user_id, post_id=like_data.post_id)
        return Response('Like successfully deleted')


    async def get_statistic_for_period(self,
                                       start_date: datetime.date,
                                       end_date: datetime.date) -> int:
        return await self.db_service.get_total_amount_of_likes_per_period(start_data=start_date, end_date=end_date)