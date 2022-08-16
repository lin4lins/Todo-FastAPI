from Exceptions import RootException


class UserException(RootException):
    pass


class UsersNotFoundException(UserException):
    """ Raises if there are not any users in database"""

    def __init__(self):
        self.detail = "Users in database not found"


class UserNotFoundException(UserException):
    """ Raises if user with some id or username is not found in database"""

    def __init__(self, user_id=None, username=None):
        if user_id:
            self.detail = f"User with id={user_id} is not registered"

        if username:
            self.detail = f"User with username={username} is not registered"

        if not user_id and not username:
            self.detail = f"User is not registered"
