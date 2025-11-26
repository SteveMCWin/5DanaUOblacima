import datetime as dt
from models import student, canteen, reservation


class DB:
    # all created students: key is id: int, value is student class
    students: dict
    # all created canteens: key is id: int, value is canteen class
    canteens: dict
    # all created reservations: key is id: int, value is reservation class
    reservations: dict
    # holds num of reservations for each canteen. the key is the id of the canteen
    # canteen_capacities[canteen_id] is another dict, where the key is the string
    # representation of the date and time
    # canteen_capacities[canteen_id][datetime_str] is how many people have reserved
    # a spot
    canteen_capacities: dict
    # dict of lists. dist key is canteen_id, list elements are
    # ids of the reservations
    # used for easier deletion of the reservations once a canteen is deleted
    canteen_reservations: dict
    # keeps track of a students reservations. key is student_id
    # value is another dict which has a key that is a string representation
    # of the time and date 
    # so if student_reservations[st_id][datetime_str] exists
    # then the student has a reservation at that time-point
    student_reservations: dict
    # these keep track of ids so ids are unique
    next_student_id: int
    next_canteen_id: int
    next_reservation_id: int

    # keep track of data that needs to be unique
    emails: set
    canteen_locations: set
    canteen_names: set

    def __init__(self):
        self.students = {}
        self.canteens = {}
        self.reservations = {}
        self.canteen_capacities = {}
        self.canteen_reservations = {}
        self.student_reservations = {}
        self.next_student_id = 1
        self.next_canteen_id = 1
        self.next_reservation_id = 1
        self.emails = set()
        self.canteen_locations = set()
        self.canteen_names = set()

    def store_student(self, s: student.Student):
        if s.email in self.emails:
            raise ValueError(
                "User with email {} already exists".format(s.email))

        s.id = self.next_student_id
        self.students[s.id] = s
        self.emails.add(s.email)

        self.next_student_id += 1
        # init dict that keeps track of reservations a student makes
        self.student_reservations[s.id] = {}

    def retrieve_student(self, id: int):
        if id in self.students:
            return self.students[id]
        raise ValueError(
            "Student with id {} isn't stored in memory".format(id))

    def isStudentAdmin(self, id: int):
        s = self.retrieve_student(id)
        return s.isAdmin

    def init_canteen_capacities(self, ct_id: int):
        self.canteen_capacities[ct_id] = {}

    def init_canteen_reservations(self, ct_id: int):
        self.canteen_reservations[ct_id] = []

    def init_student_reservations(self, student_id: int):
        self.student_reservations[student_id] = {}

    def store_canteen(self, ct: canteen.Canteen, student_id: int):
        if not self.isStudentAdmin(student_id):
            raise ValueError(
                "Student {} does not have admin priviledges".format(student_id))

        if ct.name in self.canteen_names:
            raise ValueError("Canteen named {} already exists".format(ct.name))

        if ct.location in self.canteen_locations:
            raise ValueError(
                "There is already a canteen at location {}".format(ct.location))

        ct.id = self.next_canteen_id
        self.canteens[ct.id] = ct

        self.canteen_names.add(ct.name)
        self.canteen_locations.add(ct.location)
        self.next_canteen_id += 1

        self.init_canteen_reservations(ct.id)
        self.init_canteen_capacities(ct.id)

    def retrieve_canteen(self, id: int):
        if id in self.canteens:
            return self.canteens[id]
        raise ValueError(
            "Canteen with id {} isn't stored in memory".format(id))

    def retrieve_all_canteens(self):
        return self.canteens.values()

    def update_canteen(self, ct: canteen.Canteen, student_id: int):
        if not self.isStudentAdmin(student_id):
            raise ValueError(
                "Student {} does not have admin priviledges".format(student_id))
        if not (ct.id in self.canteens):
            raise ValueError("There is no canteen with id {}".format(ct.id))

        # make sure that if location changes, we stop keeping track of it
        if ct.location != self.canteens[ct.id].location:
            self.canteen_locations.remove(self.canteens[ct.id].location)
            self.canteen_locations.add(ct.location)
        # same goes for the name
        if ct.name != self.canteens[ct.id].name:
            self.canteen_names.remove(self.canteens[ct.id].name)
            self.canteen_names.add(ct.name)

        self.canteens[ct.id] = ct
        return self.canteens[ct.id]

    def delete_canteen(self, ct_id: int, student_id: int):
        if not self.isStudentAdmin(student_id):
            raise ValueError(
                "Student {} does not have admin priviledges".format(student_id))
        if not (ct_id in self.canteens):
            raise ValueError("There is no canteen with id {}".format(ct_id))

        # remember to delete all reservations if we delete the canteen
        for r_id in self.canteen_reservations[ct_id]:
            self.delete_reservation(r_id, student_id)
        self.canteen_locations.remove(self.canteens[ct_id].location)
        self.canteen_names.remove(self.canteens[ct_id].name)
        self.canteens.pop(ct_id)
        self.canteen_capacities.pop(ct_id)

    def isDateInThePast(self, d: dt.date, t: dt.time):
        dt_reservation = dt.datetime.combine(d, t)
        return dt_reservation < dt.datetime.now()

    # the naming is a bit misleading, here we are just updating
    # the number of reservations, not linking them with canteens
    def addReservationToCanteen(self, ct_id: int, key: str):
        if key in self.canteen_capacities[ct_id]:
            self.canteen_capacities[ct_id][key] += 1
        else:
            self.canteen_capacities[ct_id][key] = 1

    # also a bit misleading
    def deleteReservationFromCanteen(self, ct_id: int, key: str):
        if not (ct_id in self.canteen_capacities):
            raise ValueError(
                "There are no reservations in canteen with id {}".format(ct_id))
        if not (key in self.canteen_capacities[ct_id]):
            raise ValueError(
                "There are no reservations in canteen with id {} at {}".format(ct_id, key))
        self.canteen_capacities[ct_id][key] -= 1
        if self.canteen_capacities[ct_id][key] < 0:
            self.canteen_capacities[ct_id][key] = 0

    def handleNewCanteenReservation(self, ct_id: int, r: reservation.Reservation):
        key1 = f"{r.date.isoformat()}|{r.time.strftime('%H:%M')}"
        self.addReservationToCanteen(ct_id, key1)

        self.canteen_reservations[ct_id].append(r.id)
        print(self.canteen_reservations[ct_id])

        # note that the way I've designed this is that we only see
        # time in increments of 30 minutes. so if a student
        # will be in the canteen for more than 30 mintes, we have
        # to update the next time-point as well
        if r.duration == 60:
            dt_combined = dt.datetime.combine(r.date, r.time)
            dt_plus_30 = dt_combined + dt.timedelta(minutes=30)
            key2 = f"{dt_plus_30.date().isoformat()}|{
                dt_plus_30.time().strftime('%H:%M')}"
            self.addReservationToCanteen(ct_id, key2)

    def handleDeleteCanteenReservation(self, ct_id: int, r: reservation.Reservation):
        key1 = f"{r.date.isoformat()}|{r.time.strftime('%H:%M')}"
        self.deleteReservationFromCanteen(ct_id, key1)

        self.canteen_reservations[ct_id].remove(r.id)
        print(self.canteen_reservations[ct_id])

        if r.duration == 60:
            dt_combined = dt.datetime.combine(r.date, r.time)
            dt_plus_30 = dt_combined + dt.timedelta(minutes=30)
            key2 = f"{dt_plus_30.date().isoformat()}|{
                dt_plus_30.time().strftime('%H:%M')}"
            self.deleteReservationFromCanteen(ct_id, key2)

    # a bit misleading, we aren't linking the reservation to the
    # student, we are just saying "this student has a reservation
    # at this date and time"
    def addReservationToStudent(self, student_id: int, key: str):
        if not (student_id in self.students):
            raise ValueError(
                "Student with id {} isn't stored in the db".format(student_id))
        self.student_reservations[student_id][key] = True

    def deleteReservationFromStudent(self, student_id: int, key: str):
        if not (student_id in self.students):
            raise ValueError(
                "Student with id {} isn't stored in the db".format(student_id))
        if not (key in self.student_reservations[student_id]):
            raise ValueError(
                "Student with id {} doesn't have a reservation at {}".format(student_id, key))
        self.student_reservations[student_id].pop(key)

    # same as canteen reservations, we are looking at time in 30 minute increments
    def handleNewStudentReservation(self, student_id: int, r: reservation.Reservation):
        key1 = f"{r.date.isoformat()}|{r.time.strftime('%H:%M')}"
        self.addReservationToStudent(student_id, key1)

        if r.duration == 60:
            dt_combined = dt.datetime.combine(r.date, r.time)
            dt_plus_30 = dt_combined + dt.timedelta(minutes=30)
            key2 = f"{dt_plus_30.date().isoformat()}|{
                dt_plus_30.time().strftime('%H:%M')}"
            self.addReservationToStudent(student_id, key2)

    def handleDeleteStudentReservation(self, student_id: int, r: reservation.Reservation):
        key1 = f"{r.date.isoformat()}|{r.time.strftime('%H:%M')}"
        self.deleteReservationFromStudent(student_id, key1)

        if r.duration == 60:
            dt_combined = dt.datetime.combine(r.date, r.time)
            dt_plus_30 = dt_combined + dt.timedelta(minutes=30)
            key2 = f"{dt_plus_30.date().isoformat()}|{
                dt_plus_30.time().strftime('%H:%M')}"
            self.deleteReservationFromStudent(student_id, key2)

    # returns true if the student has another reservation
    # at the same date and time as the passed reservation
    def doesReservationOverlap(self, r: reservation.Reservation):
        key1 = f"{r.date.isoformat()}|{r.time.strftime('%H:%M')}"
        if key1 in self.student_reservations[r.studentId]:
            return True

        if r.duration == 60:
            dt_combined = dt.datetime.combine(r.date, r.time)
            dt_plus_30 = dt_combined + dt.timedelta(minutes=30)
            key2 = f"{dt_plus_30.date().isoformat()}|{
                dt_plus_30.time().strftime('%H:%M')}"
            return key2 in self.student_reservations[r.studentId]

        return False

    # returns true if specified time and duration fits into
    # the working hours (slots) of a canteen
    def isValidMealTime(self, r: reservation.Reservation):
        r_start_dt = dt.datetime.combine(r.date, r.time)
        r_end_dt = r_start_dt + dt.timedelta(minutes=r.duration)

        ct = self.retrieve_canteen(r.canteenId)
        for m in ct.workingHours:
            meal_start_dt = dt.datetime.combine(r.date, m.from_)
            meal_end_dt = dt.datetime.combine(r.date, m.to)
            if (meal_start_dt <= r_start_dt) and (meal_end_dt >= r_end_dt):
                return True

        return False

    # returns true if max capacity reached for time-point or
    # time-points specified in reservation
    def isCanteenFull(self, r: reservation.Reservation):
        ct = self.retrieve_canteen(r.canteenId)
        key1 = f"{r.date.isoformat()}|{r.time.strftime('%H:%M')}"
        if key1 not in self.canteen_capacities[ct.id]:
            if r.duration != 60:
                return False
        elif self.canteen_capacities[ct.id][key1] >= ct.capacity:
            return True

        if r.duration != 60:
            return False

        dt_combined = dt.datetime.combine(r.date, r.time)
        dt_plus_30 = dt_combined + dt.timedelta(minutes=30)
        key2 = f"{dt_plus_30.date().isoformat()}|{
            dt_plus_30.time().strftime('%H:%M')}"
        if key2 not in self.canteen_capacities[ct.id]:
            return False
        return self.canteen_capacities[ct.id][key2] >= ct.capacity

    def store_reservation(self, r: reservation.Reservation):
        if not (r.studentId in self.students):
            raise ValueError(
                "Student with id {} isn't stored in memory".format(r.studentId))
        if not (r.canteenId in self.canteens):
            raise ValueError(
                "Canteen with id {} isn't stored in memory".format(r.canteenId))

        if self.isDateInThePast(r.date, r.time):
            raise ValueError(
                "Cannot make reservations in the past")
        if self.doesReservationOverlap(r):
            raise ValueError("User cannot have two reservations that overlap")
        if not self.isValidMealTime(r):
            raise ValueError(
                "Canteen isn't open at the specified date and time")
        if self.isCanteenFull(r):
            raise ValueError(
                "Canteen has no free spots for the specified date and time")

        r.id = self.next_reservation_id
        self.reservations[r.id] = r

        self.next_reservation_id += 1

        self.handleNewCanteenReservation(r.canteenId, r)
        self.handleNewStudentReservation(r.studentId, r)

    def retrieve_reservation(self, r_id: int):
        exists = r_id in self.reservations
        if exists:
            valid_status = self.reservations[r_id].status == "Active"

        if exists and valid_status:
            return self.reservations[r_id]

        raise ValueError(
            "Reservation with id {} isn't stored in memory".format(id))

    def delete_reservation(self, r_id: int, student_id: int):
        r = self.retrieve_reservation(r_id)
        if r.studentId != student_id and not self.isStudentAdmin(student_id):
            raise PermissionError(
                "Students can delete only their own reservations")

        r.status = "Cancelled"

        self.handleDeleteCanteenReservation(
            r.canteenId, r)
        self.handleDeleteStudentReservation(
            r.studentId, r)

        return r

    # return the name of the meal (e.g. 'dorucak') based on the
    # time. so if 'dorucak' lasts from 09:00 to 10:00, the function
    # returns 'dorucak' when you pass in 09:30
    def getCanteenMealName(self, ct_id: int, t: dt.time):
        ct = self.retrieve_canteen(ct_id)
        for m in ct.workingHours:
            if (m.from_ <= t) and (m.to > t):
                return m.meal

        return ""

    # returns remaining capacities for a canteen for the time and date intervals specified
    # incrementing the time from 'startTime' to 'dateTime' by 'duration' minutes
    def get_canteen_cap_status(self, ct_id: int, startDate: dt.date, endDate: dt.date, startTime: dt.time, endTime: dt.time, duration: int):
        if duration != 30 and duration != 60:
            raise ValueError("The duration must be either 30 or 60 (minutes)")
        res = canteen.CanteenCapacities(canteenId=ct_id, slots=[])

        current_date = startDate
        while current_date <= endDate:
            curr_time = dt.datetime.combine(current_date, startTime)
            end_datetime = dt.datetime.combine(current_date, endTime)

            while curr_time < end_datetime:
                t = curr_time.time()
                d = curr_time.date()
                meal_name = self.getCanteenMealName(ct_id, t)
                if meal_name == "":
                    curr_time += dt.timedelta(minutes=duration)
                    continue

                ct = self.retrieve_canteen(ct_id)
                remaining_cap = ct.capacity
                key = f"{d.isoformat()}|{t.strftime('%H:%M')}"
                if key in self.canteen_capacities[ct_id]:
                    remaining_cap = ct.capacity - \
                        self.canteen_capacities[ct_id][key]

                res.slots.append(canteen.CapacityResponse(
                    date=d, meal=meal_name, startTime=t, remainingCapacity=remaining_cap))

                curr_time += dt.timedelta(minutes=duration)

            current_date += dt.timedelta(days=1)

        return res

    # runs the above function for all canteens currently stored in db
    def get_all_canteens_cap_status(self, startDate: dt.date, endDate: dt.date, startTime: dt.time, endTime: dt.time, duration: int):
        res = []
        for ct_id in self.canteens:
            res.append(self.get_canteen_cap_status(
                ct_id, startDate, endDate, startTime, endTime, duration))

        return res
