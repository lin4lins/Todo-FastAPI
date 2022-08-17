from Exceptions import RootException


class DBException(RootException):
    pass


class UserTodoNotFound(DBException):
    """ Raises if user with some id do not have todo with some id """

    def __init__(self):
        self.detail = f"You do not have this todo"


class ValueNotUniqueException(DBException):
    """ Raises if user with some username is already exist in database """

    def __init__(self):
        self.detail = f"User with this email or username is already registered"
