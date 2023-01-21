import datetime
import uuid

from pydantic import BaseModel


class BaseLike(BaseModel):
    post_id: uuid.UUID


class CreateLike(BaseLike):
    pass


class DeleteLike(BaseLike):
    pass


class Like(BaseLike):
    id: int
    user_id: uuid.UUID
    date: datetime.date
