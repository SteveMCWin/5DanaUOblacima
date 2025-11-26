from pydantic import BaseModel
from typing import Optional
import datetime as dt


class Reservation(BaseModel):
    id: Optional[int] = None
    canteenId: int
    studentId: int
    date: dt.date
    time: dt.time
    duration: int
    status: str = "Active"
