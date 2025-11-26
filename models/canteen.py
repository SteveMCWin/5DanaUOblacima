from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time


class Meal(BaseModel):
    meal: str
    from_: time = Field(alias="from")
    to: time


class Canteen(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    workingHours: Optional[list[Meal]] = None


class CapacityResponse(BaseModel):
    date: date
    meal: str
    startTime: time
    remainingCapacity: int


class CanteenCapacities(BaseModel):
    canteenId: int
    slots: list[CapacityResponse]
