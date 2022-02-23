class Event:

    def __init__(self, section, length, description):
        self.section = section
        self.length = length
        self.description = description
        self.timeslot = None
        self.room = None

    def __str__(self):
        return f"{self.description}"

    def schedule(self, timeslot, room):
        self.timeslot = timeslot
        self.room = room
