from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, JSONResponse

from Authorization.password_crypt import check_password_match, \
    check_current_password_match, update_user_password
from Authorization.token_manager import get_active_current_user_from_request
from Database.db_properties import get_session
from Exceptions.TokenExceptions import TokenException
from Exceptions.UserExceptions import PasswordNotMatchException, \
    IncorrectPasswordException
from Models.ChangePasswordJSON import ChangePasswordJSON
from Routers.todos import templates

router = APIRouter(prefix="/users", tags=["user"], responses={401: {"user": "Not authorized"}})


@router.get("/change_password", response_class=HTMLResponse)
async def change_password_page(request: Request, session: Session = Depends(get_session)):
    try:
        user = await get_active_current_user_from_request(request, session)
        page = "change_password.html"
        context = {"request": request, "is_active": True}

    except TokenException as exp:
        page = "error.html"
        context = {"request": request, 'error': exp.get_detail()}

    return templates.TemplateResponse(name=page, context=context)


@router.put("/change_password", response_class=JSONResponse)
async def change_password(request: Request, session: Session = Depends(get_session)):
    try:
        user = await get_active_current_user_from_request(request, session)
        json = ChangePasswordJSON(request)
        await json.get_auth_data()
        await check_current_password_match(user, json.current_password, session)
        await check_password_match(json.new_password, json.new_password2)
        await update_user_password(json.new_password, user, session)
        content = {"url": "/todos/read"}

    except (TokenException, PasswordNotMatchException, IncorrectPasswordException) as exp:
        content = {"error": exp.get_detail()}

    return JSONResponse(content=content)
