day_dictionary = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}


class TimeSlot:
    def __init__(self, day, slotno):
        self.day = day
        self.slotno = slotno

    def __eq__(self, time_slot):
        if self.day == time_slot.day and self.slotno == time_slot.slotno:
            return True
        return False

    def __ne__(self, time_slot):
        return not (self == time_slot)

    def __str__(self):
        return f"{day_dictionary[self.day]} {self.slotno + 8}"
