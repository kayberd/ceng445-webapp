class Conflict:

    def __init__(self, conflict_type, room, instructor, attendee):
        self.type = conflict_type
        self.room = room
        self.instructor = instructor
        self.attendee = attendee
        self.offset = 0

    def __str__(self):
        if self.type == "room":
            return f"Room Conflict: {self.room}"
        if self.type == "instructor":
            return f"instructor Conflict: {self.instructor}"
        if self.type == "attendee":
            return f"Attendee Conflict: {self.attendee}"
