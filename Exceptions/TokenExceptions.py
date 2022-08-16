from Exceptions import RootException


class TokenException(RootException):

    def __init__(self):
        self.detail = f"You are not authorized"


class InvalidTokenException(TokenException):
    """ Raises if user_id(sub) or/and username was not found in token"""

    def __init__(self):
        self.detail = f"Invalid token"


class ExpiredTokenException(TokenException):
    """ Raises if token expired: expire datetime is larger than now datetime"""

    def __init__(self):
        self.detail = f"Session expired"


class IncorrectUsernameOrPasswordException(TokenException):
    """ Raises if there is a user with such username, but password is incorrect
        User might input either incorrect username or incorrect password or both"""

    def __init__(self):
        self.detail = f"Incorrect username or password"


class TokenNotFoundException(TokenException):
    """ Raises if token not found in cookies"""

    def __init__(self):
        self.detail = f"Unauthorized session"
