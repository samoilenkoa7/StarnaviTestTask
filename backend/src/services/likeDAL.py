import datetime
import uuid

from fastapi import Depends, HTTPException


from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from src import models
from src.database import get_session


class LikeDAL:
    """Class for database operations with likes"""

    EXCEPTION = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail='Like with provided user id and post id was not found')

    def __init__(self,
                 db_session: AsyncSession = Depends(get_session),):
        self.session = db_session

    async def create_like(self,
                          user_id: uuid.UUID,
                          post_id: uuid.UUID) -> models.PostLike:
        statement = select(models.User).filter(models.User.id == user_id)
        user_instance = await self.session.execute(statement)
        user = user_instance.scalars().first()
        statement = select(models.Post).filter(models.Post.id == post_id)
        post_instance = await self.session.execute(statement)
        post = post_instance.scalars().first()
        user.liked_posts.append(post)
        await self.session.commit()
        return user

    async def delete_like(self,
                          user_id: uuid.UUID,
                          post_id: uuid.UUID) -> None:
        """Code duplication of getting user model, because async sqlalchemy
        returning greenlet error when calling 2+ sessions and I can inject userDAL class"""
        statement = select(models.User)\
            .filter(models.User.id == user_id, models.User.liked_posts.any(id=post_id))
        user_instance = await self.session.execute(statement)
        user = user_instance.scalars().one_or_none()
        if user is None:
            raise self.EXCEPTION
        user.liked_posts = [instance for instance in user.liked_posts if instance.id != post_id]
        self.session.add(user)
        await self.session.commit()

    async def get_total_amount_of_likes_per_period(self,
                                                   start_data: datetime.date,
                                                   end_date: datetime.date) -> int:
        statement = select(func.count()).select_from(models.PostLike)\
            .filter(models.PostLike.c.date >= start_data, models.PostLike.c.date <= end_date)
        amount_of_likes = await self.session.execute(statement)
        amount_of_likes = amount_of_likes.scalars()
        amount_of_likes = [i for i in amount_of_likes]
        return amount_of_likes[0]
