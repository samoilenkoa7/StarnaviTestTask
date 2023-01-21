import datetime
import uuid

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import get_session
from src.models import User

from src.pydantic_models import user as user_model


class UserDAL:
    """User data accel layer for database
     operations with user model"""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_user(self, user_data: user_model.CreateUser) -> User:
        """Creating User instance and adding to session"""
        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            last_login=user_data.last_login,
            last_request=user_data.last_request,
            username=user_data.username,
            hashed_password=user_data.password
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_user_by_username(self, username: str):
        statement = select(User).where(User.username == username)
        users = await self.session.execute(statement)
        users = users.scalars()
        user = users.one()
        return user

    async def update_user_last_login_time(self,
                                          user_instance: User,
                                          current_time: datetime.datetime = datetime.datetime.utcnow()) -> None:
        user_instance.last_login = current_time
        self.session.add(user_instance)
        await self.session.commit()

    async def update_user_last_request_time(self,
                                            user_id: uuid.UUID,
                                            current_time: datetime.datetime = datetime.datetime.utcnow()) -> None:
        user_instance = await self.get_user_by_id(user_id=user_id)
        user_instance.last_request = current_time
        self.session.add(user_instance)
        await self.session.commit()

    async def get_user_by_id(self,
                             user_id: uuid.UUID) -> User:
        statement = select(User).filter(User.id == user_id)
        user_instance = await self.session.execute(statement)
        user = user_instance.scalars().one()
        return user
