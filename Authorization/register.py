from Authorization.password_crypt import get_password_hash
from Database.db_manager import add_user
from Models.RegisterJSON import RegisterJSON
from Models.User import RawUser
from sqlalchemy.orm import Session


async def register_user(json: RegisterJSON, session: Session):
    hashed_password = get_password_hash(json.password)
    user = RawUser(email=json.email, username=json.username,
                   first_name=json.first_name, last_name=json.last_name,
                   password=hashed_password, is_active=False)
    add_user(user, session)
