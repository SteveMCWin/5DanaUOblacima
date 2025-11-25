from pydantic import BaseModel, Field
from datetime import time


class Meal(BaseModel):
    meal: str
    from_: time = Field(alias="from")
    to: time


class Canteen(BaseModel):
    id: int | None = None
    name: str
    location: str
    capacity: int
    workingHours: list[Meal]
