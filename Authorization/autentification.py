from typing import Union

from Database.db_init import DatabaseUser
from Database.db_manager import get_user_by_username
from sqlalchemy.orm import Session

from Authorization.password_crypt import verify_password
from Exceptions.TokenExceptions import IncorrectUsernameOrPasswordException
from Exceptions.UserExceptions import UserNotFoundException


def get_authenticated_user(username: str, password: str, session: Session) \
                                            -> Union[DatabaseUser, None]:
    user = get_user_by_username(username, session)
    if not user:
        raise UserNotFoundException(username)

    if not authenticate_user(user, password):
        raise IncorrectUsernameOrPasswordException()

    return user


def authenticate_user(user: DatabaseUser, password_to_check: str) -> bool:
    true_hashed_password = user.hashed_password
    if not verify_password(password_to_check, true_hashed_password):
        return False

    return True
