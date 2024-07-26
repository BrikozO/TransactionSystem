from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer

from app.backend.querys import AsyncORM
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models import User


class Authorization:
    TOKEN_URI = OAuth2PasswordBearer(tokenUrl='auth/login')

    @classmethod
    async def authenticate_user(cls, email: str, password: str) -> User:
        user = await AsyncORM.get_user_by_auth(email, password)
        if user is not None:
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')

    @classmethod
    async def create_access_token(cls, data: dict) -> str:
        to_encode: dict = data.copy()
        moscow_timezone: timezone = timezone(offset=timedelta(hours=3))
        expire = datetime.now(tz=moscow_timezone) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({'exp': expire})
        jwt_token: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return jwt_token
