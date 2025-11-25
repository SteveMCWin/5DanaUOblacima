from models import student, canteen


class DB:
    students: dict
    canteens: dict
    reservations: dict
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
        self.next_student_id = 1
        self.next_canteen_id = 1
        self.next_reservation_id = 1
        self.emails = set()
        self.canteen_locations = set()
        self.canteen_names = set()

    def store_student(self, s: student):
        if s.email in self.emails:
            raise ValueError(
                "User with email {} already exists".format(s.email))

        s.id = self.next_student_id
        self.students[s.id] = s
        self.emails.add(s.email)

        self.next_student_id += 1

    def retrieve_student(self, id: int):
        if id in self.students:
            return self.students[id]
        raise ValueError(
            "Student with id {} isn't stored in memory".format(id))

    def update_student(self, s: student):
        if not (s.id in self.students):
            raise ValueError("Student with id {} isn't stored in memory".format(id))
        self.students[s.id] = s

    def store_canteen(self, ct: canteen.Canteen, s: student.Student):
        if not s.isAdmin:
            raise ValueError("Student {} does not have admin priviledges".format(s.id))

        if ct.name in self.canteen_names: 
            raise ValueError("Canteen named {} already exists".format(ct.name))

        if ct.location in self.canteen_locations:
            raise ValueError("There is already a canteen at location {}".format(ct.location))

        ct.id = self.next_canteen_id
        self.canteens[ct.id] = ct

        self.canteen_names.add(ct.name)
        self.canteen_locations.add(ct.location)
        self.next_canteen_id += 1

    def retrieve_canteen(self, id: int):
        if id in self.canteens:
            return self.canteens[id]
        raise ValueError(
            "Canteen with id {} isn't stored in memory".format(id))

    def retrieve_all_canteens(self):
        return self.canteens.values()
