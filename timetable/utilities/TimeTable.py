import copy
import itertools
from typing import List
from prettytable import PrettyTable, prettytable

from .Conflict.AttendeeConflict import AttendeeConflict
from .Conflict.ConflictReport import ConflictReport
from .Event import Event
from .Conflict.InstructorConflict import InstructorConflict
from .Conflict.RoomConflict import RoomConflict
from .TimeSlot import TimeSlot


class TimeTable:
    """Events are stored in 2D array of lists(In other words 3D array)
    If an added event doesn't scheduled yet, it is appended to the nonscheduled_events.
    And it will be removed from that list once it is scheduled.
    instructor_list keeps record of instructor to make it easier to check instructor conflicts.
    List is populated when the addEvent happens. It is not removed when the event removed since there can be
    other events with same instructor. TimeTable starts from 8 AM(with slotOffset default value it is 8:40 AM)"""

    def __init__(self, days, slotsperday, rooms, slotoffset=40):
        self.days = days
        self.slotsPerDay = slotsperday
        self.rooms = rooms
        self.slotOffset = slotoffset
        self.event_3d_array = [[[] for _ in range(slotsperday)] for _ in range(days)]
        self.nonscheduled_events = list()
        self.instructor_list = list()

    def __str__(self):
        pretty = PrettyTable()
        pretty.field_names = [" ", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        for i in range(self.slotsPerDay):
            row = [f"{i + 8}:{self.slotOffset}"]
            for j in range(self.days):
                if not self.event_3d_array[j][i]:
                    row.append(str(self.event_3d_array[j][i]))
                else:
                    cell = ""
                    for event in self.event_3d_array[j][i]:
                        cell += str(event) + "\n"
                    row.append(cell)
            pretty.add_row(row)

        return pretty.__str__() + "\n"


    def str_html(self):
        pretty = []
        dayList = [[" "], ["MON"], ["TUE"], ["WED"], ["THU"], ["FRI"], ["SAT"], ["SUN"]]
        pretty.append(dayList[:self.days+1])

        for i in range(self.slotsPerDay):
            row = [[f"{i + 8}:{self.slotOffset}"]]
            for j in range(self.days):
                # if not self.event_3d_array[j][i]:
                #     row.append(str(self.event_3d_array[j][i]))
                # else:
                    # cell = ""
                    # for event in self.event_3d_array[j][i]:
                    #     cell += str(event) + "\n"
                    # row.append(cell)

                cell = []
                for event in self.event_3d_array[j][i]:
                    cell.append(str(event))
                row.append(cell)
            pretty.append(row)

        return pretty

    """If event is not scheduled yet, it will be added to the nonscheduled_events list. 
    If it is scheduled it will be inserted to the relevant part of event_3d_array.
    If the event's instructor is not yet added to the instructor_list, this function also appends the instructor."""

    def addEvents(self, eventlist):
        for given_event in eventlist:
            if given_event.timeslot is None:
                self.nonscheduled_events.append(given_event)
            elif given_event not in self.event_3d_array[given_event.timeslot.day][given_event.timeslot.slotno]:
                for slot in range(given_event.length):
                    self.event_3d_array[given_event.timeslot.day][given_event.timeslot.slotno + slot].append(
                        given_event)

            if given_event.section.instr not in self.instructor_list:
                self.instructor_list.append(given_event.section.instr)

            if given_event.room not in self.rooms.room_list:
                self.rooms.room_list.append(given_event.room)

    """If the given event exists in the TimeTable, it will be removed from nonscheduled_events or event_3d_array"""

    def removeEvents(self, eventlist):
        for given_event in eventlist:
            if given_event.timeslot is None:
                self.nonscheduled_events.remove(given_event)

            if given_event in self.event_3d_array[given_event.timeslot.day][given_event.timeslot.slotno]:
                for slot in range(given_event.length):
                    self.event_3d_array[given_event.timeslot.day][given_event.timeslot.slotno + slot].remove(
                        given_event)

    """This method finds all conflicts and return a ConflictReport with iterating through the event_3d_array 
    by filtering with rooms, instructors, and attendees. """

    def getConflicts(self):
        conflict_report = ConflictReport()

        for day_index in range(len(self.event_3d_array)):
            day = self.event_3d_array[day_index]
            time: List[Event]
            for time_index in range(len(day)):
                time = day[time_index]
                # Loops through rooms and finds a conflict
                # if there are more than one events in the same room at the same time-slot
                for room in self.rooms.room_list:
                    room_conflict_event_list = list(filter(lambda e: e.room == room, time))
                    if len(room_conflict_event_list) > 1:
                        room_conflict = RoomConflict("room", room, None, None, TimeSlot(day_index, time_index),
                                                     room_conflict_event_list)
                        conflict_report.major_conflicts.append(room_conflict)
                # Loops through instructors and finds a conflict
                # if there are more than one events with the same instructor at the same time-slot
                for instructor in self.instructor_list:
                    instructor_conflict_event_list = list(filter(lambda e: e.section.instr == instructor, time))
                    if len(instructor_conflict_event_list) > 1:
                        instructor_conflict = InstructorConflict("instructor", None, instructor, None,
                                                                 instructor, TimeSlot(day_index, time_index),
                                                                 instructor_conflict_event_list)
                        conflict_report.major_conflicts.append(instructor_conflict)

                # Student lists are added to a dictionary using their indexes in the time-slot
                # for enabling further use which will be explained few lines ahead
                # copy is used to keep section.student_list integrity
                student_lists_dict = {}
                for i in range(len(time)):
                    student_lists_dict[i] = copy.copy(time[i].section.student_list)

                # Iteration through the subsets of list of list of students ordered by descending sizes
                for i in range(len(student_lists_dict), 1, -1):
                    # List of dictionary which stores all subsets size = i
                    student_list_subset_dict_list = list(
                        map(dict, itertools.combinations(student_lists_dict.items(), i)))

                    # Iteration through these subsets
                    for lst_index in range(len(student_list_subset_dict_list)):

                        student_list_subset_dict = student_list_subset_dict_list[lst_index]
                        student_list_subset_list = [*student_list_subset_dict.values()]
                        # Finding conflicting students
                        students_conflicted = set(student_list_subset_list[0]).intersection(*student_list_subset_list)

                        if len(students_conflicted) > 0:
                            students_events = []
                            # Finds these students events for report creation
                            # and removes them from the student_list_dict
                            # to block conflict duplications. Removing does not effect section.student_list
                            # since copy.copy() method is used in the creation process of this list
                            for j in range(len(time)):
                                if students_conflicted.issubset(time[j].section.student_list):
                                    students_events.append(time[j])
                                    for student in students_conflicted:
                                        student_lists_dict[j].remove(student)

                            attendee_conflict = AttendeeConflict("attendee", None, None, None, students_events,
                                                                 TimeSlot(day_index, time_index), students_conflicted)

                            conflict_report.minor_conflicts.append(attendee_conflict)

        conflict_report.number_of_major = len(conflict_report.major_conflicts)
        conflict_report.number_of_minor = len(conflict_report.minor_conflicts)
        conflict_report.set_offset(self.slotOffset)  # slotOffset sent to the conflict report for printing properly
        return conflict_report

    """If the event is not already assigned to that particular timeslot before, 
    It will be assigned with this method and it will be removed from nonscheduled_events list."""

    def assign(self, timeslot, event):
        if event.room not in self.rooms.room_list:
            raise Exception("The room is not in the rooms_list.")
        event.timeslot = timeslot
        if event not in self.event_3d_array[timeslot.day][timeslot.slotno]:
            for slot in range(event.length):
                self.event_3d_array[timeslot.day][timeslot.slotno + slot].append(event)
        if event in self.nonscheduled_events:
            self.nonscheduled_events.remove(event)

    """Since the events are already properly formatted this method can 
    easily returns a list element from event_3d_array"""

    def getEventsAt(self, timeslot):
        return self.event_3d_array[timeslot.day][timeslot.slotno]

    def updateView(self):
        pass

    """
        Generates a prettier looking table
    """
