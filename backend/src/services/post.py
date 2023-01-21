import uuid

from fastapi import Depends, Response

from src import models
from src.pydantic_models.post import CreatePost, LikePost
from src.services.postDAL import PostDAL


class PostService:
    def __init__(self, db_service: PostDAL = Depends()):
        self.db_service = db_service

    async def create_new_post(self,
                              post_data: CreatePost,
                              user_id: uuid.UUID) -> models.Post:
        new_post = await self.db_service.create_new_post(post_data, user_id)
        return new_post

    async def like_post(self,
                        post_data: LikePost) -> Response:
        current_likes = await self.db_service.like_post(post_data.id)
        return Response(f'Current amount on post with id {post_data.id}: {current_likes}')

    async def unlike_post(self,
                          post_data: LikePost) -> Response:
        current_likes = await self.db_service.unlike_post(post_data.id)
        return Response(f'Current amount on post with id {post_data.id}: {current_likes}')