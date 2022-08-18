import os
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from Authorization.autentification import get_authenticated_user
from Database.db_init import DatabaseUser
from fastapi import Request
from jose import JWTError, jwt

from Database.db_manager import update_user_status, get_user_status
from Exceptions.TokenExceptions import TokenException, TokenNotFoundException
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
        expires = datetime.timestamp(datetime.now() + timedelta(minutes=1))

    encode.update({"exp": expires})
    print(key, algorithm)
    token = jwt.encode(encode, key=key, algorithm=algorithm)
    return token


async def get_current_user(request: Request) -> CurrentUser:
    try:
        access_token = await get_access_token_from_request(request)
        payload = jwt.decode(access_token, key=os.environ.get("SECRET_KEY"),
                             algorithms=[os.environ.get("ALGORITHM")])
        user_id: int = int(payload.get("sub"))
        username: str = payload.get("username")
        if user_id is None or username is None:
            raise JWTError()

        return CurrentUser(id=user_id, username=username)

    except (AttributeError, JWTError):
        raise TokenException()


async def authorize_user(username: str, password: str, session: Session):
    authenticated_user = get_authenticated_user(username, password, session)
    update_user_status(authenticated_user, True, session)
    return get_token(authenticated_user, expires_delta=timedelta(minutes=30))


async def is_user_active(request: Request, session) -> bool:
    user: CurrentUser = await get_current_user(request)
    is_active = get_user_status(user, session)
    return is_active


async def get_active_current_user_from_request(request: Request, session) -> CurrentUser:
    user: CurrentUser = await get_current_user(request)
    is_active = get_user_status(user, session)
    if not is_active:
        raise TokenException()

    return user


async def get_access_token_from_request(request: Request) -> str:
    cookie = request.cookies
    access_token = cookie.get('access_token')
    if not access_token:
        raise TokenNotFoundException()

    return access_token
