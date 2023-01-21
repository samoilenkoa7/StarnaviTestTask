from typing import Optional

from fastapi import APIRouter, Depends

from src import models
from src.pydantic_models.post import Post, CreatePost, LikePost
from src.services.auth import get_current_user, AuthService
from src.services.post import PostService

router = APIRouter(
    prefix='/posts'
)


@router.post('/create', response_model=Post)
async def create_new_post(
        post_data: CreatePost,
        user: models.User = Depends(get_current_user),
        service: PostService = Depends(),
):
    return await service.create_new_post(post_data, user.id)
