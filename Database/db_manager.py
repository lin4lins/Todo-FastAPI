from Exceptions.DBExceptions import UserTodosNotFoundException, UserTodoNotFound
from Exceptions.UserExceptions import UsersNotFoundException, UserNotFoundException
from Models.Todo import RawTodo
from Models.User import CurrentUser
from sqlalchemy.orm import Session

from Database.db_init import DatabaseTodo, DatabaseUser


def get_all_user_todos_by_user_id(user_id: int, session: Session) -> list:
    todos = session.query(DatabaseTodo).filter(DatabaseTodo.owner_id == user_id).all()
    if not todos:
        raise UserTodosNotFoundException(user_id)

    return todos


def get_todo_by_id_and_user_id(todo_id: int, user_id: int, session: Session) \
        -> DatabaseTodo:
    todo = session.query(DatabaseTodo). \
        filter(DatabaseTodo.id == todo_id). \
        filter(DatabaseTodo.owner_id == user_id).first()
    if not todo:
        raise UserTodoNotFound(user_id, todo_id)

    return todo


def create_todo(user_id: int, todo: RawTodo, session: Session) -> None:
    todo_to_create = DatabaseTodo(title=todo.title, description=todo.description,
                                  priority=todo.priority, complete=todo.complete,
                                  owner_id=user_id)
    session.add(todo_to_create)
    session.flush()
    session.commit()


def update_todo(todo_id: int, user_id: int, todo: RawTodo, session: Session) -> None:
    todo_to_update = get_todo_by_id_and_user_id(todo_id, user_id, session)

    todo_to_update.title = todo.title
    todo_to_update.description = todo.description
    todo_to_update.priority = todo.priority
    session.commit()


def update_todo_status(todo_id: int, user_id: int, is_complete: bool, session: Session) -> None:
    todo_to_update = get_todo_by_id_and_user_id(todo_id, user_id, session)
    todo_to_update.complete = is_complete
    session.commit()


def remove_todo(todo_id: int, user_id: int, session: Session) -> None:
    todo_to_delete = get_todo_by_id_and_user_id(todo_id, user_id, session)
    session.delete(todo_to_delete)
    session.commit()


# USERS
def get_all_users(session: Session) -> list[DatabaseUser]:
    users = session.query(DatabaseUser).all()
    if not users:
        raise UsersNotFoundException()

    return users


def get_user_by_id(id: int, session: Session) -> DatabaseUser:
    user = session.query(DatabaseUser).filter(DatabaseUser.id == id).first()
    if not user:
        raise UserNotFoundException(id)

    return user


def get_user_by_username(username: str, session: Session) -> DatabaseUser:
    user = session.query(DatabaseUser).filter(DatabaseUser.username == username).first()
    if not user:
        raise UserNotFoundException(username)

    return user


def update_user_password(user: CurrentUser, password: str, session: Session) -> None:
    user = session.query(DatabaseUser). \
        filter(DatabaseUser.username == user.username
               and DatabaseUser.id == user.id).first()
    user.hashed_password = password
    session.commit()
    return


def delete_user(user: CurrentUser, session: Session) -> None:
    user_to_delete = session.query(DatabaseUser). \
        filter(DatabaseUser.username == user.username
               and DatabaseUser.id == user.id).first()
    session.delete(user_to_delete)
    session.commit()
    return
