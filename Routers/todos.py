from starlette.responses import JSONResponse

from Authorization.token_manager import get_active_current_user_from_request
from Database.db_manager import (add_todo, remove_todo,
                                 get_todo_by_id_and_user_id,
                                 update_todo, update_todo_status,
                                 get_all_user_todos_by_user_id)
from Database.db_properties import get_session
from fastapi import APIRouter, Depends, Request
from fastapi.params import Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from Exceptions.DBExceptions import UserTodoNotFound
from Exceptions.TokenExceptions import TokenException
from Models.Todo import RawTodo
from sqlalchemy.orm import Session


router = APIRouter(prefix="/todos", tags=["todo"],
                   responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory="templates")


@router.get("/read", response_class=HTMLResponse)
async def read_todos(request: Request, session: Session = Depends(get_session)):
    try:
        user = await get_active_current_user_from_request(request, session)
        todos = get_all_user_todos_by_user_id(user.id, session)
        page = "home.html"
        context = {"request": request, "todos": todos, 'is_active': True}

    except TokenException:
        page = "error.html"
        context = {"request": request, 'error': 'You are unauthorized'}

    return templates.TemplateResponse(name=page, context=context)


@router.get("/add", response_class=HTMLResponse)
async def add_todo(request: Request, session: Session = Depends(get_session)):
    try:
        user = await get_active_current_user_from_request(request, session)
        page = "add-todo.html"
        context = {"request": request, "is_active": True}

    except TokenException as exp:
        page = "error.html"
        context = {"request": request, 'error': exp.get_detail()}

    return templates.TemplateResponse(name=page, context=context)


@router.post("/add", response_class=JSONResponse)
async def add_todo(request: Request, todo: RawTodo,
                   session: Session = Depends(get_session)):
    try:
        user = await get_active_current_user_from_request(request, session)
        add_todo(user.id, todo, session)
        content = {"url": "/todos/read"}

    except TokenException as exp:
        content = {"error": exp.get_detail()}

    return JSONResponse(content=content)


@router.get("/edit/{id}", response_class=HTMLResponse)
async def edit_todo(request: Request, id: int = Path(...),
                    session: Session = Depends(get_session)):
    try:
        user = await get_active_current_user_from_request(request, session)
        todo_to_update = get_todo_by_id_and_user_id(id, user.id, session)
        page = "edit-todo.html"
        context = {"request": request, "todo": todo_to_update, "is_active": True}

    except (TokenException, UserTodoNotFound) as exp:
        page = "error.html"
        context = {"request": request, 'error': exp.get_detail()}

    return templates.TemplateResponse(name=page, context=context)


@router.put("/edit/{id}", response_class=JSONResponse)
async def edit_todo(request: Request, todo: RawTodo, id: int = Path(...),
                    session: Session = Depends(get_session)):
    try:
        user = await get_active_current_user_from_request(request, session)
        update_todo(id, user.id, todo, session)
        content = {"url": "/todos/read"}

    except (TokenException, UserTodoNotFound) as exp:
        content = {"error": exp.get_detail()}

    return JSONResponse(content=content)


@router.delete("/delete/{id}", response_class=JSONResponse)
async def delete_todo(request: Request, id: int = Path(...),
                       session: Session = Depends(get_session)):
    try:
        user = await get_active_current_user_from_request(request, session)
        remove_todo(id, user.id, session)
        content = {"url": "/todos/read"}

    except (TokenException, UserTodoNotFound) as exp:
        content = {"error": exp.get_detail()}

    return JSONResponse(content=content)


@router.put("/complete/{id}", response_class=JSONResponse)
async def update_todo_completion_status(request: Request,
                                        status: dict, id: int = Path(...),
                                        session: Session = Depends(get_session)):
    try:
        user = await get_active_current_user_from_request(request, session)
        todo_status = status.get("completed")
        if todo_status is not None:
            update_todo_status(id, user.id, todo_status, session)

        content = {"url": "/todos/read"}

    except (TokenException, UserTodoNotFound) as exp:
        content = {"error": exp.get_detail()}

    return JSONResponse(content=content)




