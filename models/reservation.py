from pydantic import BaseModel, field_serializer
import datetime as dt


class Reservation(BaseModel):
    id: int = 0
    canteenId: int
    studentId: int
    date: dt.date
    time: dt.time
    duration: int
    status: str = "Active"

    @field_serializer("time")
    def serialize_time(self, value: dt.time):
        return value.strftime("%H:%M")
