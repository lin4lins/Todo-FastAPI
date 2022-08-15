from typing import Union

from Authorization.password_crypt import get_password_hash
from Authorization.token_manager import get_current_user
from Database.db_init import DatabaseUser
from Database.db_manager import (delete_user, get_all_users, get_user_by_id,
                                 update_user_password)
from Database.db_properties import get_session
from fastapi import APIRouter, Depends
from fastapi.params import Form, Path, Query
from Models.User import CurrentUser
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["user"])


@router.get("")
async def get_users(id: int = Query(None), session: Session = Depends(get_session))\
                                                            -> list[DatabaseUser]:
    if not id:
        return get_all_users(session)

    user = get_user_by_id(id, session)
    if not user:
        raise get_user_not_found_exception(id)

    return user


@router.get("/{id}")
async def get_user(id: int = Path(...), session: Session = Depends(get_session))\
                                                    -> Union[DatabaseUser, None]:
    user = get_user_by_id(id, session)
    if not user:
        raise get_user_not_found_exception(id)

    return user


@router.put("/change_password")
async def change_password(new_password: str = Form(...),
                          user: CurrentUser = Depends(get_current_user),
                          session: Session = Depends(get_session)) -> dict:
    if not user:
        raise get_user_exception()

    hashed_password = get_password_hash(new_password)
    update_user_password(user, hashed_password, session)
    return {"Message": "Password has been changed successfully"}


@router.delete("/delete_account")
async def delete_account(user: CurrentUser = Depends(get_current_user),
                         session: Session = Depends(get_session)) -> dict:
    if not user:
        raise get_user_exception()

    delete_user(user, session)
    return {"Message": "Account has been deleted successfully"}
