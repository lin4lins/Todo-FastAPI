from typing import Union

from starlette.responses import RedirectResponse

from Authorization.token_manager import get_current_user
from Database.db_init import DatabaseTodo
from Database.db_manager import (get_all_todos,
                                 get_all_user_todos_by_user_id,
                                 get_todo_by_id_and_user_id)
from Database.db_properties import get_session
from Exceptions import (get_todo_not_found_exception,
                        get_user_do_not_have_todos_exception,
                        get_user_exception)
from fastapi import APIRouter, Depends, Request, Form
from fastapi.params import Path, Query
from Models.Todo import RawTodo
from Models.User import CurrentUser
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status

router = APIRouter(prefix="/todos", tags=["todo"],
                   responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory="templates")


@router.get("/read", response_class=HTMLResponse)
async def read_user_todos(request: Request,
                          session: Session = Depends(get_session)):
    todos = get_all_todos(session)
    return templates.TemplateResponse(name="home.html",
                                      context={"request": request, "todos": todos})


@router.get("/add", response_class=HTMLResponse)
async def add_todo(request: Request):
    return templates.TemplateResponse(name="add-todo.html", context={"request": request})


@router.post("/add")
async def add_new_todo(todo: RawTodo,
                       session: Session = Depends(get_session)):
    todo_to_create = DatabaseTodo(title=todo.title, description=todo.description,
                                  priority=todo.priority, complete=todo.complete,
                                  owner_id=1)
    session.add(todo_to_create)
    session.flush()
    session.commit()
    return RedirectResponse(url="/todos/read", status_code=status.HTTP_302_FOUND)


@router.get("/edit/{id}", response_class=HTMLResponse)
async def edit_todo(request: Request, id: int = Path(...),
                    session: Session = Depends(get_session)):
    todo_to_update = get_todo_by_id_and_user_id(id, 1, session)

    return templates.TemplateResponse(name="edit-todo.html",
                                      context={"request": request,
                                               "todo": todo_to_update})


@router.post("/edit/{id}")
async def edit_todo(todo: RawTodo, id: int = Path(...),
                    session: Session = Depends(get_session)):
    todo_to_update = get_todo_by_id_and_user_id(id, 1, session)

    todo_to_update.title = todo.title
    todo_to_update.description = todo.description
    todo_to_update.priority = todo.priority
    session.commit()
    return RedirectResponse(url="/todos/read", status_code=status.HTTP_302_FOUND)


# ----------- fastAPI METHODS
@router.get("/all", deprecated=True)
async def read_all_todos(session: Session = Depends(get_session)) \
        -> Union[list[DatabaseTodo], None]:
    return get_all_todos(session)


@router.get("")
async def read_user_todos(id: int = Query(None),
                          user: CurrentUser = Depends(get_current_user),
                          session: Session = Depends(get_session)) \
        -> Union[DatabaseTodo, list[DatabaseTodo], None]:
    if not user:
        raise get_user_exception()

    if id:
        todos = get_todo_by_id_and_user_id(id, user.id, session)
    else:
        todos = get_all_user_todos_by_user_id(user.id, session)

    if not todos:
        raise get_user_do_not_have_todos_exception(id)

    return todos


@router.post("", status_code=201)
async def create_todo(todo: RawTodo, user: CurrentUser = Depends(get_current_user),
                      session: Session = Depends(get_session)) -> dict:
    if not user:
        raise get_user_exception()

    todo_to_create = DatabaseTodo(title=todo.title, description=todo.description,
                                  priority=todo.priority, complete=todo.complete,
                                  owner_id=user.id)
    session.add(todo_to_create)
    session.flush()
    session.commit()
    return {"Message": "Todo has been created successfully", "id": todo_to_create.id}


@router.put("/{id}")
async def update_todo(todo: RawTodo, id: int = Path(...),
                      user: CurrentUser = Depends(get_current_user),
                      session: Session = Depends(get_session)) -> dict:
    if not user:
        raise get_user_exception()

    todo_to_update = get_todo_by_id_and_user_id(id, user.id, session)
    if not todo_to_update:
        raise get_todo_not_found_exception(id)

    todo_to_update.title = todo.title
    todo_to_update.description = todo.description
    todo_to_update.priority = todo.priority
    todo_to_update.complete = todo.complete
    session.commit()
    return {"Message": "Todo has been edited successfully", "id": todo_to_update.id}


@router.delete("/{id}")
async def delete_todo(id: int = Path(...),
                      user: CurrentUser = Depends(get_current_user),
                      session: Session = Depends(get_session)) -> dict:
    if not user:
        raise get_user_exception()

    todo_to_delete = get_todo_by_id_and_user_id(id, user.id, session)
    if not todo_to_delete:
        raise get_todo_not_found_exception(id)

    session.delete(todo_to_delete)
    session.commit()
    return {"Message": "Todo has been deleted successfully", "id": todo_to_delete.id}
