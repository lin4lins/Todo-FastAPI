from passlib.context import CryptContext
from sqlalchemy.orm import Session

from Database.db_init import DatabaseUser
from Database.db_manager import get_user_by_id_and_username, update_password
from Exceptions.UserExceptions import PasswordNotMatchException, \
    IncorrectPasswordException
from Models.User import CurrentUser

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


async def check_password_match(password1: str, password2: str) -> None:
    if not password1 == password2:
        raise PasswordNotMatchException()


async def check_current_password_match(user: CurrentUser, input_current_password: str,
                                       session: Session) -> None:
    user: DatabaseUser = get_user_by_id_and_username(user.id, user.username, session)
    if not verify_password(input_current_password, user.hashed_password):
        raise IncorrectPasswordException()


async def update_user_password(new_plain_password: str, user: CurrentUser,
                               session: Session):
    hashed_password = get_password_hash(new_plain_password)
    update_password(user, hashed_password, session)
