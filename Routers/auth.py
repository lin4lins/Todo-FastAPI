from Authorization.password_crypt import get_password_hash
from Authorization.token_manager import authorize_user, get_current_user
from Database.db_init import DatabaseUser
from Database.db_manager import update_user_status
from Database.db_properties import get_session
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse

from Exceptions.TokenExceptions import TokenException
from Exceptions.UserExceptions import UserNotFoundException
from Models.LoginJSON import LoginJSON
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


@router.post("/")
async def login(request: Request,
                session: Session = Depends(get_session)):
    try:
        json = LoginJSON(request)
        await json.get_auth_data()
        token = await authorize_user(json.username, json.password, session)
        content = {"url": "/todos/read"}
        response = JSONResponse(content=content)
        response.set_cookie(key="access_token", value=token, httponly=True)

    except (TokenException, UserNotFoundException) as exp:
        response = JSONResponse(content=exp.get_detail())

    return response


@router.post("/logout")
async def logout(request: Request, session: Session = Depends(get_session)):
    try:
        user = await get_current_user(request)
        update_user_status(user, False, session)
        content = {"url": "/"}
        response = JSONResponse(content=content)
        response.delete_cookie("access_token")

    except (TokenException, UserNotFoundException) as exp:
        response = JSONResponse(content=exp.get_detail())

    return response


# -----------
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
