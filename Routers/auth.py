from datetime import timedelta

from Authorization.autentification import get_authenticated_user
from Authorization.password_crypt import get_password_hash
from Authorization.token_manager import get_token
from Database.db_init import DatabaseUser
from Database.db_properties import get_session
from Exceptions import get_token_exception
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from Models.User import RawUser
from sqlalchemy.orm import Session

from Routers.todos import templates

router = APIRouter(tags=["auth"],
                   responses={401: {"user": "Not authorized"}})


@router.get("/", response_class=HTMLResponse)
async def authpage(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})


@router.get("/register", response_class=HTMLResponse)
async def regpage(request: Request):
    return templates.TemplateResponse(name="register.html", context={"request": request})


@router.post("/signin", status_code=201)
async def create_user(user: RawUser, session: Session = Depends(get_session)) -> dict:
    hashed_password = get_password_hash(user.password)
    user_to_add = DatabaseUser(email=user.email, username=user.username,
                               first_name=user.first_name, last_name=user.last_name,
                               hashed_password=hashed_password, is_active=True)
    session.add(user_to_add)
    session.flush()
    session.commit()
    return {"Message": "User has been created successfully", "id": user_to_add.id}


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: Session = Depends(get_session)) -> dict:
    username = form_data.username
    pure_unconfirmed_password = form_data.password

    authenticated_user = get_authenticated_user(username, pure_unconfirmed_password,
                                                session)
    if not authenticated_user:
        raise get_token_exception()

    return {"Message": "User has been logged in successfully",
            "token": get_token(authenticated_user, expires_delta=timedelta(minutes=20))}
