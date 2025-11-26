from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List
from datetime import date, time


class Meal(BaseModel):
    meal: str
    from_: time = Field(alias="from")
    to: time

    @field_serializer("from_", "to")
    def serialize_time(self, value: time):
        return value.strftime("%H:%M")

class Canteen(BaseModel):
    id: int = 0
    name: str
    location: str
    capacity: int
    workingHours: list[Meal]

class CanteenPut(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    workingHours: Optional[List[Meal]] = None


class CapacityResponse(BaseModel):
    date: date
    meal: str
    startTime: time
    remainingCapacity: int

    @field_serializer("startTime")
    def serialize_time(self, value: time):
        return value.strftime("%H:%M")

class CanteenCapacities(BaseModel):
    canteenId: int
    slots: list[CapacityResponse]
