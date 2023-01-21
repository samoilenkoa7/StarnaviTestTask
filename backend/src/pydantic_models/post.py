import uuid

from pydantic import BaseModel


class BasePost(BaseModel):
    title: str


class LikePost(BaseModel):
    id: uuid.UUID


class CreatePost(BasePost):
    pass


class Post(BasePost):
    id: uuid.UUID
    owner_id: uuid.UUID

    class Config:
        orm_mode = True
