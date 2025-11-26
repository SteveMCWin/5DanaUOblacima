from pydantic import BaseModel


class Student(BaseModel):
    id: int = 0
    name: str
    email: str
    isAdmin: bool
