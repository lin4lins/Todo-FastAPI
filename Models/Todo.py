from typing import Optional

from pydantic import BaseModel, Field


class RawTodo(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = Field(ge=1, le=5)
    complete: bool = False