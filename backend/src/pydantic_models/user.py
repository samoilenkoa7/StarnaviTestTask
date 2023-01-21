import datetime
import uuid

from pydantic import BaseModel


class BaseUser(BaseModel):
    first_name: str
    last_name: str


class CreateUser(BaseUser):
    username: str
    password: str
    last_login: datetime.datetime = datetime.datetime.utcnow()
    last_request: datetime.datetime = datetime.datetime.utcnow()


class UserStatistic(BaseUser):
    last_login: datetime.datetime
    last_request: datetime.datetime

    class Config:
        orm_mode = True


class User(BaseUser):
    id: uuid.UUID

    class Config:
        orm_mode = True
