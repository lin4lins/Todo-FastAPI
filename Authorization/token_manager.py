import os
from datetime import datetime, timedelta
from typing import Optional

from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session

from Authorization.autentification import get_authenticated_user
from Database.db_init import DatabaseUser
from fastapi import Request
from jose import JWTError, jwt

from Database.db_manager import update_user_status
from Exceptions import RootException
from Exceptions.TokenExceptions import InvalidTokenException
from Models.User import CurrentUser


def get_token(user: DatabaseUser, expires_delta: timedelta) -> str:
    token = create_access_token(user.username, user.id,
                                os.environ.get("SECRET_KEY"), os.environ.get("ALGORITHM"),
                                expires_delta)
    return token


def create_access_token(username: str, user_id: int,
                        key: str, algorithm: str,
                        expires_delta: Optional[timedelta] = None) -> str:
    encode = {"sub": str(user_id), "username": username}
    if expires_delta:
        expires = datetime.timestamp(datetime.now() + expires_delta)
    else:
        expires = datetime.timestamp(datetime.now() + timedelta(minutes=20))

    encode.update({"exp": expires})
    token = jwt.encode(encode, key=key, algorithm=algorithm)
    return token


async def get_current_user(request: Request) -> CurrentUser:
    try:
        access_token = request.cookies.get("access_token")
        payload = jwt.decode(access_token, key=os.environ.get("SECRET_KEY"),
                             algorithms=[os.environ.get("ALGORITHM")])
        user_id: int = int(payload.get("sub"))
        username: str = payload.get("username")
        if user_id is None or username is None:
            raise JWTError()

        return CurrentUser(id=user_id, username=username)

    except (AttributeError, ExpiredSignatureError, JWTError):
        raise TokenException()


async def authorize_user(username: str, password: str, session: Session):
    try:
        authenticated_user = get_authenticated_user(username, password, session)
        update_user_status(authenticated_user, True, session)
        return get_token(authenticated_user, expires_delta=timedelta(minutes=15))

    except RootException as exp:
        return exp.get_detail()
