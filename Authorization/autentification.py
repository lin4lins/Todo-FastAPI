from typing import Union

from Database.db_init import DatabaseUser
from Database.db_manager import get_user_by_username
from Exceptions import get_user_not_found_exception
from sqlalchemy.orm import Session

from Authorization.password_crypt import verify_password


def get_authenticated_user(username: str, password: str, session: Session) \
                                            -> Union[DatabaseUser, None]:
    database_user = get_user_by_username(username, session)
    if not database_user:
        raise get_user_not_found_exception()
        
    if authenticate_user(database_user, password):
        return database_user

    return


def authenticate_user(user: DatabaseUser, password_to_check: str) -> bool:
    true_hashed_password = user.hashed_password
    if not verify_password(password_to_check, true_hashed_password):
        return False

    return True
