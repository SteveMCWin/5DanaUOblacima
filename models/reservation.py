import datetime as dt


class Reservation:
    canteen_id: int
    student_id: int
    start_time: dt.datetime
    duration: dt.timedelta
    is_canceled: bool

    def __init__(self, canteen_id, student_id, start_time, duration):
        self.canteen_id = canteen_id
        self.student_id = student_id
        self.start_time = start_time
        self.duration = duration
        self.is_canceled = False
