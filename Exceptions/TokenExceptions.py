from Exceptions import RootException


class ExpiredTokenException(RootException):
    """ Raises if token expired: expire datetime is larger than now datetime"""

    def __init__(self):
        self.detail = f"Session expired"


class InvalidTokenException(RootException):
    """ Raises if user_id(sub) or/and username was not found in token"""

    def __init__(self):
        self.detail = f"Invalid token"


class IncorrectUsernameOrPasswordException(RootException):
    """ Raises if there is a user with such username, but password is incorrect
        User might input either incorrect username or incorrect password or both"""

    def __init__(self):
        self.detail = f"Incorrect username or password"


class TokenNotFoundException(RootException):
    """ Raises if token not found in cookies"""

    def __init__(self):
        self.detail = f"Unauthorized session"
