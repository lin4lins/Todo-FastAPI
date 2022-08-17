from Authorization.password_crypt import check_password_match
from Authorization.register import register_user
from Authorization.token_manager import authorize_user, get_current_user
from Database.db_manager import update_user_status
from Database.db_properties import get_session
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse

from Exceptions.DBExceptions import ValueNotUniqueException
from Exceptions.TokenExceptions import TokenException
from Exceptions.UserExceptions import UserNotFoundException, UserException, \
    PasswordNotMatchException
from Models.LoginJSON import LoginJSON
from Models.RegisterJSON import RegisterJSON
from sqlalchemy.orm import Session

from Routers.todos import templates

router = APIRouter(tags=["auth"],
                   responses={401: {"user": "Not authorized"}})


@router.get("/", response_class=HTMLResponse)
async def authpage(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})


@router.get("/signin", response_class=HTMLResponse)
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

    except (TokenException, UserException) as exp:
        content = {"error": exp.get_detail()}
        response = JSONResponse(content=content)

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


@router.post("/signin")
async def signin(request: Request, session: Session = Depends(get_session)):
    try:
        json = RegisterJSON(request)
        await json.get_auth_data()
        await check_password_match(json.password, json.password2)
        await register_user(json, session)
        content = {"url": "/"}

    except (ValueNotUniqueException, PasswordNotMatchException) as exp:
        content = {"error": exp.get_detail()}

    response = JSONResponse(content=content)
    return response
