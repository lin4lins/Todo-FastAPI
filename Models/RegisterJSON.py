from typing import Optional
from fastapi import Request


class RegisterJSON:

    def __init__(self, request: Request):
        self.request: Request = request
        self.email: Optional[str] = None
        self.username: Optional[str] = None
        self.first_name: Optional[str] = None
        self.last_name: Optional[str] = None
        self.password: Optional[str] = None
        self.password2: Optional[str] = None

    async def get_auth_data(self):
        json = await self.request.json()
        self.email = json.get("email")
        self.username = json.get("username")
        self.first_name = json.get("first_name")
        self.last_name = json.get("last_name")
        self.password = json.get("password")
        self.password2 = json.get("password2")
