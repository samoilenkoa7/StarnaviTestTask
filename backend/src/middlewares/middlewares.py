import datetime

from fastapi import Request, HTTPException
from jose import jwt, JWTError
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from src import models
from src.database import async_session
from sqlalchemy.future import select
from src.settings import settings


class CustomMiddleware(BaseHTTPMiddleware):
    def __init__(self,
                 app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer'):
            token = token.split(' ')
            token = token[1]
            try:
                play_load = jwt.decode(
                    token,
                    settings.jwt_secret,
                    algorithms=[settings.jwt_algorithm]
                )
            except JWTError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Provided credentials are not valid')
            user_data = play_load.get('user')
            session = async_session()
            statement = select(models.User).filter(models.User.id == user_data.get('id'))
            user_instance = await session.execute(statement)
            user = user_instance.scalars().one()
            user.last_request = datetime.datetime.utcnow()
            session.add(user)
            await session.commit()
            await session.close()
        response = await call_next(request)
        return response
