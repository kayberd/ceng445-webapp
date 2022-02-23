from .Conflict import Conflict


class AttendeeConflict(Conflict):
    def __init__(self, conflict_type, room, instructor, attendee, event_list, time_slot, attendee_list):
        super().__init__(conflict_type, room, instructor, attendee)
        self.event_list = event_list
        self.time_slot = time_slot
        self.attendee_list = attendee_list

    def __str__(self):
        a = "Attendee Conflict for attendees: "
        for attendee in self.attendee_list:
            a += str(attendee) + " "
        a += ", For events: "
        for event in self.event_list:
            a += str(event) + " "
        a += f"at {self.time_slot}:{self.offset}"

        return a
