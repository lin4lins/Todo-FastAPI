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


def get_token_expired_exception():
    token_expired_exception = \
        HTTPException(status_code=404, detail=f"Token expired")
    return token_expired_exception
