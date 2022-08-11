import os
from datetime import datetime, timedelta
from typing import Optional, Union

from sqlalchemy.orm import Session

from Authorization.autentification import get_authenticated_user
from Database.db_init import DatabaseUser
from Exceptions import get_token_expired_exception, get_user_exception, \
    get_token_exception
from fastapi import Depends
from jose import JWTError, jwt
from Models.User import CurrentUser

from Authorization.password_crypt import oauth2_bearer


def get_token(user: DatabaseUser, expires_delta: timedelta) -> str:
    token = create_access_token(user.username, user.id,
                                os.environ.get("SECRET_KEY"), os.environ.get("ALGORITHM"),
                                expires_delta)
    return token


def create_access_token(username: str, user_id: int,
                        key, algorithm,
                        expires_delta: Optional[timedelta] = None) -> str:
    encode = {"sub": str(user_id), "username": username}
    if expires_delta:
        expires = datetime.now() + expires_delta
    else:
        expires = datetime.now() + timedelta(minutes=20)

    encode.update({"exp": expires})
    return jwt.encode(encode, key=key, algorithm=algorithm)


async def get_current_user(token: str = Depends(oauth2_bearer))\
                                    -> Union[CurrentUser, None]:
    try:
        payload = jwt.decode(token, key=os.environ.get("SECRET_KEY"),
                             algorithms=[os.environ.get("ALGORITHM")])
        user_id: int = int(payload.get("sub"))
        username: str = payload.get("username")
        if user_id is None or username is None:
            raise get_user_exception()

        return CurrentUser(id=user_id, username=username)

    except jwt.ExpiredSignatureError:
        raise get_token_expired_exception()
    except JWTError:
        raise get_user_exception()


async def authorize_user(username: str, password: str, session: Session):
    authenticated_user = get_authenticated_user(username, password, session)
    if not authenticated_user:
        raise get_token_exception()

    return get_token(authenticated_user, expires_delta=timedelta(minutes=60))
