from fastapi import HTTPException


def get_user_exception() -> HTTPException:
    credentials_exception = HTTPException(status_code=401,
                                          detail="Could not found validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return credentials_exception


def get_token_exception() -> HTTPException:
    token_exception = HTTPException(status_code=401,
                                    detail="Incorrect username or password",
                                    headers={"WWW-Authenticate": "Bearer"})
    return token_exception


def get_user_not_found_exception(id: int = None) -> HTTPException:
    user_not_found_exception = HTTPException(status_code=404,
                                             detail=f"User with id {id} not found")
    return user_not_found_exception


def get_users_do_not_exist_exception() -> HTTPException:
    users_do_not_exist_exception = HTTPException(status_code=404,
                                                 detail=f"Users do not exist")
    return users_do_not_exist_exception


def get_user_do_not_have_todos_exception(id: int) -> HTTPException:
    user_do_not_have_todos_exception = \
        HTTPException(status_code=404, detail=f"User with id {id} do not have todos")
    return user_do_not_have_todos_exception


def get_todo_not_found_exception(todo_id: int) -> HTTPException:
    todo_not_found_exception = \
        HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return todo_not_found_exception


def get_token_expired_exception():
    token_expired_exception = \
        HTTPException(status_code=404, detail=f"Token expired")
    return token_expired_exception
