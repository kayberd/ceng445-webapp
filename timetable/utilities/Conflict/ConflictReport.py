class ConflictReport:
    def __init__(self):
        self.major_conflicts = list()
        self.minor_conflicts = list()
        self.number_of_minor = 0
        self.number_of_major = 0

    def __str__(self):
        report = f"<text>Major conflicts = {self.number_of_major}</text><br/>"

        for conflict in self.major_conflicts:
            report +='<text>' + str(conflict) + '</text></br>' 

        report += f"<text>Minor conflicts: {self.number_of_minor} </text><br/>"

        for conflict in self.minor_conflicts:
            report += '<text>' + str(conflict) + '</text><br/>'

        return report

    def set_offset(self, offset):
        for major in self.major_conflicts:
            major.offset = offset
        for minor in self.minor_conflicts:
            minor.offset = offset
