from starlette.responses import JSONResponse

from Authorization.token_manager import get_current_user
from Database.db_manager import (create_todo, remove_todo,
                                 get_todo_by_id_and_user_id,
                                 update_todo, update_todo_status,
                                 get_all_user_todos_by_user_id)
from Database.db_properties import get_session
from fastapi import APIRouter, Depends, Request
from fastapi.params import Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from Exceptions import RootException
from Exceptions.TokenExceptions import InvalidTokenException
from Models.Todo import RawTodo
from sqlalchemy.orm import Session


router = APIRouter(prefix="/todos", tags=["todo"],
                   responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory="templates")


@router.get("/read", response_class=HTMLResponse)
async def read_todos(request: Request, session: Session = Depends(get_session)):
    try:
        user = await get_current_user(request)
        todos = get_all_user_todos_by_user_id(user.id, session)
        page = "home.html"
        context = {"request": request, "todos": todos, 'user': True}

    except InvalidTokenException:
        page = "error.html"
        context = {"request": request, 'error': 'You are unauthorized'}

    except Exception:
        page = "error.html"
        context = {"request": request, 'error': 'Something went wrong'}
    return templates.TemplateResponse(name=page, context=context)


@router.get("/add", response_class=HTMLResponse)
async def add_todo(request: Request):
    return templates.TemplateResponse(name="add-todo.html", context={"request": request})


@router.post("/add", response_class=JSONResponse)
async def add_todo(request: Request, todo: RawTodo,
                   session: Session = Depends(get_session)):
    try:
        user = await get_current_user(request)
        create_todo(user.id, todo, session)
        content = {"url": "/todos/read"}

    except RootException as exp:
        content = {"error": exp.detail}

    return JSONResponse(content=content)


@router.get("/edit/{id}", response_class=HTMLResponse)
async def edit_todo(request: Request, id: int = Path(...),
                    session: Session = Depends(get_session)):
    try:
        user = await get_current_user(request)
        todo_to_update = get_todo_by_id_and_user_id(id, user.id, session)
        page = "edit-todo.html"
        context = {"request": request, "todo": todo_to_update}

    except RootException as exp:
        page = "error.html"
        context = {"request": request, 'error': exp.detail}

    return templates.TemplateResponse(name=page, context=context)


@router.put("/edit/{id}", response_class=JSONResponse)
async def edit_todo(request: Request, todo: RawTodo, id: int = Path(...),
                    session: Session = Depends(get_session)):
    try:
        user = await get_current_user(request)
        update_todo(id, user.id, todo, session)
        content = {"url": "/todos/read"}

    except RootException as exp:
        content = {'error': exp.detail}

    return JSONResponse(content=content)

@router.delete("/delete/{id}")
async def delete_todo(id: int = Path(...), user: CurrentUser = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    remove_todo(id, user.id, session)
    return JSONResponse(content={"url": "/todos/read"})


@router.put("/complete/{id}", response_class=HTMLResponse)
async def update_todo_completion_status(diction: dict, id: int = Path(...),
                        user: CurrentUser = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    todo_status = diction["completed"]
    if todo_status is not None:
        update_todo_status(id, user.id, todo_status, session)

    return JSONResponse({"url": "/todos/read"})




