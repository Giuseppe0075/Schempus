from tabulate import tabulate

class Course:
    def __init__(self, name, professor, number_of_students, hours_for_week):
        self.name = name
        self.professor = professor
        self.number_of_students = number_of_students
        self.hours_for_week = hours_for_week

    def __str__(self):
        return f"{self.name} by {self.professor}"


class Classroom:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

    def __str__(self):
        return f"{self.name}"

class Timetable:
    """This class represents the timetable of a university"""

    def __init__(self, classrooms, courses):
        import random as rd
        self.classrooms = classrooms
        self.courses = courses
        self.timetable = []
        for course in courses:
            _course = []
            for _ in range(course.hours_for_week):
                _course.append([rd.randint(0, 4), rd.randint(0, len(classrooms)-1), rd.randint(0, 7)]) #[day, classroom, hour]
            self.timetable.append(_course)

    def __str__(self):
        result = []
        for course in self.timetable:
            result.append(str(lesson) for lesson in course)
        return tabulate(result, tablefmt="plain")

    # This method prints the timetable as a table where the rows are the days, the columns are the classrooms and the cells are the hours
    def display_as_table(self) :
        table = [["" for _ in range(len(self.classrooms))] for _ in range(5)]
        for course in self.timetable :
            print(f"id: {self.timetable.index(course)} " + str(self.courses[self.timetable.index(course)]))
            for lesson in course :
                day, classroom, hour = lesson
                table[day][
                    classroom] += f"{hour + 1}: {self.courses[self.timetable.index(course)].name} (ID: {self.timetable.index(course)})\n"
        print(tabulate(table, headers=[classroom.name for classroom in self.classrooms],
                       showindex=["Mon", "Tue", "Wed", "Thu", "Fri"], tablefmt="grid"))