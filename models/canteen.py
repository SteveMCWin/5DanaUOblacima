import datetime as dt


class Meal:
    name: str
    start_time: dt.time
    end_time: dt.time

    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time


class Canteen:
    id: int
    name: str
    location: str
    capacity: int
    working_hours: list[Meal]

    def __init__(self, name, location, capacity, working_hours):
        self.name = name
        self.location = location
        self.capacity = capacity
        self.working_hours = working_hours
