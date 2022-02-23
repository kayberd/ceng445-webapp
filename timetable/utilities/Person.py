class Person:
    def __init__(self, person_id, name):
        self.person_id = person_id
        self.name = name

    def __str__(self):
        return f"{self.person_id} {self.name}"
