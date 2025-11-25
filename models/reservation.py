from pydantic import BaseModel
import datetime as dt


class Reservation(BaseModel):
    canteenId: int | None = None
    studentId: int
    date: dt.date
    time: dt.time
    duration: dt.timedelta
    status: str = "Active"
