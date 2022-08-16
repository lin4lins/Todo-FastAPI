from Exceptions import RootException


class DBException(RootException):
    pass


class UserTodoNotFound(DBException):
    """ Raises if user with some id do not have todo with some id """

    def __init__(self, user_id, todo_id):
        self.detail = f"User with id={user_id} does not have todo with id={todo_id}"
