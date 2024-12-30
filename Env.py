from tabulate import tabulate

class Professor:
    """This class represents a professor in a university"""

    def __init__(self, name, free_hours):
        """This method initializes the professor with the given name"""
        self.name = name
        self.free_hours = free_hours

    def __str__(self):
        return self.name

class Course:
    """This class represents a course in a university"""

    def __init__(self, name, professor: Professor, number_of_students, hours_for_week, lab_hours = 0):
        """"This method initializes the course with the given name, professor, number of students for this particular course and hours for week"""
        self.name = name
        self.professor = professor
        self.number_of_students = number_of_students
        self.hours_for_week = hours_for_week
        self.lab_hours = lab_hours

    def __str__(self):
        return f"{self.name} by {self.professor}"


class Classroom:
    """This class represents a classroom in a university"""
    def __init__(self, name, capacity):
        """This method initializes the classroom with the given name and capacity"""
        self.name = name
        self.capacity = capacity

    def __str__(self):
        return f"{self.name}: {self.capacity}"

class Timetable:
    """This class represents the timetable of a university"""

    def __init__(self, classrooms, courses):
        """This method initializes the timetable with a list of Classroom and a list of Course"""
        import random as rd
        self.classrooms = classrooms
        self.courses = courses
        self.timetable = []
        # Generate a random timetable
        for course in courses:
            _course = []
            _lab_hours = course.lab_hours
            for _ in range(course.hours_for_week):
                # [day, classroom, hour, lab = True while lab_hours > 0 else False]
                _course.append([rd.randint(0, 4), rd.randint(0, len(classrooms)-1), rd.randint(0, 7), True if _lab_hours > 0 else False])
                _lab_hours -= 1
            self.timetable.append(_course)

    def __str__(self):
        result = []
        for course in self.timetable:
            result.append(str(lesson) for lesson in course)
        return tabulate(result, tablefmt="plain")

    def set_timetable(self, timetable):
        self.timetable = timetable


    # This method prints the timetable as a table where the rows are the days, the columns are the classrooms and the cells are the hours
    def display_as_table(self):
        table = [["" for _ in range(len(self.classrooms))] for _ in range(5)]
        for course in self.timetable:
            for lesson in course:
                day, classroom, hour, lab = lesson
                table[day][classroom] += f"{hour + 1}: {'Lab. ' if lab else ''}{self.courses[self.timetable.index(course)].name} (ID: {self.timetable.index(course)})\n"

        # Fill in free hours
        for day in range(5):
            for classroom in range(len(self.classrooms)):
                occupied_hours = [lesson[2] for course in self.timetable for lesson in course if lesson[0] == day and lesson[1] == classroom]
                for hour in range(8):
                    if hour not in occupied_hours:
                        table[day][classroom] += f"{hour + 1}: FREE\n"

        # Sort the lessons in each cell
        for day in range(5):
            for classroom in range(len(self.classrooms)):
                lessons = table[day][classroom].strip().split('\n')
                lessons.sort(key=lambda x: int(x.split(':')[0]))
                table[day][classroom] = '\n'.join(lessons)

        return tabulate(table, headers=[classroom.name for classroom in self.classrooms],
                       showindex=["Mon", "Tue", "Wed", "Thu", "Fri"], tablefmt="grid")