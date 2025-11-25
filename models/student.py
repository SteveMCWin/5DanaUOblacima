class Student:
    id: int
    name: str
    email: str
    is_admin: bool

    def __init__(self, name, email, is_admin):
        self.name = name
        self.email = email
        self.is_admin = is_admin


