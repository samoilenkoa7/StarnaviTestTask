import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select

from src import models
from src.database import get_session
from src.pydantic_models.post import CreatePost, LikePost


class PostDAL:
    """Class for database operations with posts"""
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def _get(self,
                   post_id: uuid.UUID) -> models.Post:
        statement = select(models.Post).filter(models.Post.id == post_id)
        post_instance = await self.session.execute(statement)
        post_instance = post_instance.scalars().one()
        return post_instance

    async def create_new_post(self,
                              post_data: CreatePost,
                              user_id: uuid.UUID) -> models.Post:
        new_post = models.Post(
            title=post_data.title,
            owner_id=user_id
        )
        self.session.add(new_post)
        await self.session.commit()
        return new_post

    async def get_post_by_id(self,
                             post_id: uuid.UUID) -> models.Post:
        return await self._get(post_id)
