from typing import Optional
from fastapi import Request


class ChangePasswordJSON:

    def __init__(self, request: Request):
        self.request: Request = request
        self.current_password: Optional[str] = None
        self.new_password: Optional[str] = None
        self.new_password2: Optional[str] = None

    async def get_auth_data(self):
        json = await self.request.json()
        self.current_password = json.get("current_password")
        self.new_password = json.get("new_password")
        self.new_password2 = json.get("new_password2")
