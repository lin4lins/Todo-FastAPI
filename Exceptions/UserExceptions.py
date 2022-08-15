from Exceptions import RootException


class UsersNotFoundException(RootException):
    """ Raises if there are not any users in database"""

    def __init__(self):
        self.detail = "Users in database not found"


class UserNotFoundException(RootException):
    """ Raises if user with some id or username is not found in database"""

    def __init__(self, user_id=None, username=None):
        if user_id:
            self.detail = f"User with id={user_id} not found"

        if username:
            self.detail = f"User with username={username} not found"

        if not user_id and not username:
            self.detail = f"User not found"