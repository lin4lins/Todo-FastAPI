class UserTodosNotFoundException(Exception):
    """ Raises if user has no todos in database"""

    def __init__(self, user_id):
        self.detail = f"User with id={user_id} does not have todos"
        super().__init__(self.detail)


class UserTodoNotFound(Exception):
    """ Raises if user with some id do not have todo with some id """

    def __init__(self, user_id, todo_id):
        self.detail = f"User with id={user_id} does not have todo with id={todo_id}"
        super().__init__(self.detail)