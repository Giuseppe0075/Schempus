from tabulate import tabulate

class Professor:
    """This class represents a professor in a university"""

    def __init__(self, name):
        """This method initializes the professor with the given name"""
        self.name = name

    def __str__(self):
        return self.name

class Subjects:
    COMPUTER_SCIENCE = 0
    PHYSICS = 1
    MATH = 2
    CHEMISTRY = 3
    BIOLOGY = 4
    HISTORY = 5
    GEOGRAPHY = 6
    ART = 7
    MUSIC = 8
    PHILOSOPHY = 9
    ECONOMICS = 10
    LITERATURE = 11
    SOCIOLOGY = 12
    PSYCHOLOGY = 13
    ANTHROPOLOGY = 14
    POLITICAL_SCIENCE = 15
    LINGUISTICS = 16
    ASTRONOMY = 17
    STATISTICS = 18

class Course:
    """This class represents a course in a university"""

    def __init__(self, name, professor: Professor, number_of_students, hours_for_week, subject, lab_hours = 0):
        """"This method initializes the course with the given name, professor, number of students for this particular course and hours for week"""
        self.name = name
        self.professor = professor
        self.number_of_students = number_of_students
        self.hours_for_week = hours_for_week
        self.subject = subject
        self.lab_hours = lab_hours

    def __str__(self):
        return f"{self.name} by {self.professor}"

class Classroom:
    """This class represents a classroom in a university"""
    def __init__(self, name, capacity, is_lab = False, subject = None):
        """This method initializes the classroom with the given name, capacity, wheter is laboratory or not and, if it is a laboratory, for which subject"""
        self.name = name
        self.capacity = capacity
        self.is_lab = is_lab
        if is_lab:
            self.subject = subject

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
