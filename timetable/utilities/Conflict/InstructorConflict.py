from .Conflict import Conflict


class InstructorConflict(Conflict):
    def __init__(self, conflict_type, room, instructor, attendee, instructor_name, time_slot, event_list):
        super().__init__(conflict_type, room, instructor, attendee)
        self.instructor_name = instructor_name
        self.time_slot = time_slot
        self.event_list = event_list

    def __str__(self):
        a = f"Instructor Conflict for {self.instructor_name} at {self.time_slot}:{self.offset} for events:"

        for event in self.event_list:
            a += f"{event} "
        return a
