from typing import Optional
from fastapi import Request


class LoginJSON:

    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def get_auth_data(self):
        json = await self.request.json()
        self.username = json.get("username")
        self.password = json.get("password")
