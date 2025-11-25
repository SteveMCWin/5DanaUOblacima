from pydantic import BaseModel
from typing import Optional


class Student(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    isAdmin: bool
