import os

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_bearer = OAuth2PasswordBearer(tokenUrl=os.environ.get("TOKEN_URL"))


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)
