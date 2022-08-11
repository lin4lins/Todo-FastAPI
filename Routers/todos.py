from Authorization.token_manager import get_current_user
from Database.db_manager import (create_todo, remove_todo,
                                 get_all_todos, get_todo_by_id_and_user_id,
                                 update_todo, update_todo_status)
from Database.db_properties import get_session
from fastapi import APIRouter, Depends, Request
from fastapi.params import Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from Models.Todo import RawTodo
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from Models.User import CurrentUser

router = APIRouter(prefix="/todos", tags=["todo"],
                   responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory="templates")


@router.get("/read", response_class=HTMLResponse)
async def read_todos(request: Request, user: CurrentUser = Depends(get_current_user),
                     session: Session = Depends(get_session)):
    todos = get_all_todos(user.id, session)
    return templates.TemplateResponse(name="home.html",
                                      context={"request": request, "todos": todos})


@router.get("/add", response_class=HTMLResponse)
async def add_todo(request: Request):
    return templates.TemplateResponse(name="add-todo.html", context={"request": request})


@router.post("/add")
async def add_todo(todo: RawTodo, user: CurrentUser = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    create_todo(user.id, todo, session)
    return JSONResponse(content={"url": "/todos/read"})


@router.get("/edit/{id}", response_class=HTMLResponse)
async def edit_todo(request: Request, id: int = Path(...),
                    user: CurrentUser = Depends(get_current_user),
                    session: Session = Depends(get_session)):
    todo_to_update = get_todo_by_id_and_user_id(id, user.id, session)

    return templates.TemplateResponse(name="edit-todo.html",
                                      context={"request": request,
                                               "todo": todo_to_update})


@router.put("/edit/{id}")
async def edit_todo(todo: RawTodo, id: int = Path(...),
                    user: CurrentUser = Depends(get_current_user),
                    session: Session = Depends(get_session)):
    update_todo(id, user.id, todo, session)
    return JSONResponse(content={"url": "/todos/read"})


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




