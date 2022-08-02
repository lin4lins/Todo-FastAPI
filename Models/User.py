from pydantic import BaseModel


class RawUser(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    is_active: bool = True


class CurrentUser(BaseModel):
    id: int
    username: str
