from Database.db_manager import (create_todo, delete_todo_from_db,
                                 get_all_todos, get_todo_by_id_and_user_id,
                                 set_todo_complete, update_todo)
from Database.db_properties import get_session
from fastapi import APIRouter, Depends, Request
from fastapi.params import Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from Models.Todo import RawTodo
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

router = APIRouter(prefix="/todos", tags=["todo"],
                   responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory="templates")


@router.get("/read", response_class=HTMLResponse)
async def read_todos(request: Request, session: Session = Depends(get_session)):
    todos = get_all_todos(session)
    return templates.TemplateResponse(name="home.html",
                                      context={"request": request, "todos": todos})


@router.get("/add", response_class=HTMLResponse)
async def add_todo(request: Request):
    return templates.TemplateResponse(name="add-todo.html", context={"request": request})


@router.post("/add")
async def add_todo(todo: RawTodo,
                       session: Session = Depends(get_session)):
    create_todo(todo, session)
    return JSONResponse(content={"url": "/todos/read"})


@router.get("/edit/{id}", response_class=HTMLResponse)
async def edit_todo(request: Request, id: int = Path(...),
                    session: Session = Depends(get_session)):
    todo_to_update = get_todo_by_id_and_user_id(id, 1, session)

    return templates.TemplateResponse(name="edit-todo.html",
                                      context={"request": request,
                                               "todo": todo_to_update})


@router.put("/edit/{id}")
async def edit_todo(todo: RawTodo, id: int = Path(...),
                    session: Session = Depends(get_session)):
    update_todo(id, todo, session)
    return JSONResponse(content={"url": "/todos/read"})


@router.delete("/delete/{id}")
async def delete_todo(id: int = Path(...),
                       session: Session = Depends(get_session)):
    delete_todo_from_db(id, 1, session)
    return JSONResponse(content={"url": "/todos/read"})


@router.put("/complete/{id}", response_class=HTMLResponse)
async def complete_todo(diction: dict, id: int = Path(...),
                        session: Session = Depends(get_session)):
    todo_status = diction["completed"]
    if todo_status:
        set_todo_complete(id, 1, session)

    return JSONResponse({"url": "/todos/read"})




