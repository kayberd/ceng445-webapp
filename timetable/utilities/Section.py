class Section:
    def __init__(self, courseid, currsection, totsection, desc, instr):
        self.courseid = courseid
        self.currsection = currsection
        self.totsection = totsection
        self.desc = desc
        self.instr = instr
        self.student_list = list()

    def __str__(self):
        return f"Course:{self.courseid} Section:{self.currsection}: {self.desc}"

    def addStudent(self, stlist):
        for student in stlist:
            if student not in self.student_list:
                self.student_list.append(student)

    def removeStudent(self, stlist):
        for student in stlist:
            if student in self.student_list:
                self.student_list.remove(student)
