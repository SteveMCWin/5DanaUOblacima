from models import student, canteen, reservation


class DB:
    students: dict
    canteens: dict
    reservations: dict
    canteen_reservations: dict
    student_reservations: dict
    next_student_id: int
    next_canteen_id: int
    next_reservation_id: int

    emails: set
    canteen_locations: set
    canteen_names: set

    def __init__(self):
        self.students = {}
        self.canteens = {}
        self.reservations = {}
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

        self.student_reservations[s.id] = {}

    def retrieve_student(self, id: int):
        if id in self.students:
            return self.students[id]
        raise ValueError(
            "Student with id {} isn't stored in memory".format(id))

    def isStudentAdmin(self, id: int):
        s = self.retrieve_student(id)
        return s.isAdmin

    def init_canteen_reservations(self, ct_id: int):
        self.canteen_reservations[ct_id] = {}

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

        if ct.location != self.canteens[ct.id].location:
            self.canteen_locations.remove(self.canteens[ct.id].location)
            self.canteen_locations.add(ct.location)

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

        self.canteen_locations.remove(self.canteens[ct_id].location)
        self.canteen_names.remove(self.canteens[ct_id].name)
        self.canteens.pop(ct_id)
        self.canteen_reservations.pop(ct_id)

    def doesReservationOverlap(self, r: reservation.Reservation):
        # TODO
        return False

    def isCanteenFull(self, r: reservation.Reservation):
        # TODO
        return False

    def isValidMealTime(r):
        # TODO
        return True

    def store_reservation(self, r: reservation.Reservation):
        if self.doesReservationOverlap(r):
            raise ValueError("User cannot have two reservations that overlap")
        if not self.isValidMealTime(r):
            raise ValueError(
                "Canteen isn't open at the specified date and time")
        if self.isCanteenFull(r):
            raise ValueError(
                "Canteen has no free spots for the specified date and time")

        # TODO
        # update the correct values in the canteen_reservations
        # and update the correct value from student_reservations

        r.id = self.next_reservation_id
        self.reservations[r.id] = r

        self.next_reservation_id += 1

    def retrieve_reservation(self, r_id: int):
        valid_status = False
        exists = r_id in self.reservations
        if exists:
            valid_status = self.reservations[r_id] == "Active"

        if exists and valid_status:
            return self.reservations[r_id]

        raise ValueError(
            "Reservation with id {} isn't stored in memory".format(id))

    def delete_reservation(self, r_id: int, student_id: int):
        r = self.retrieve_reservation(r_id)
        if r.studentId != student_id:
            raise PermissionError(
                "Students can delete only their own reservations")

        # TODO
        # update the correct values in the canteen_reservations
        # and update the correct value from student_reservations
