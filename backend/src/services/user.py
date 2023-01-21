import uuid

from fastapi import Depends

from src import models
from src.services.userDAL import UserDAL


class UserService:
    def __init__(self, db_service: UserDAL = Depends()):
        self.db_service = db_service

    async def get_user_statistic(self,
                                 user_id: uuid.UUID) -> models.User:
        user = await self.db_service.get_user_by_id(user_id)
        return user

    async def update_last_request_time(self,
                                       user_id: uuid.UUID) -> None:
        await self.db_service.update_user_last_request_time(user_id)
