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
        self.hours = [None] * 8

    def __str__(self):
        return f"{self.name}" + str([str(hour) if hour is not None else "None" for hour in self.hours])

class Timetable:
    """This class represents the timetable of a university"""

    def __init__(self, classrooms):
        self.classrooms = classrooms
        self.timetable = [[Classroom(classroom.name, classroom.capacity) for classroom in classrooms] for _ in range(5)]

    def first_initialization(self, courses: list):
        import random as rd
        slots = [(day, hour, classroom) for day in range(5) for classroom in range(len(self.classrooms)) for hour in
                 range(8)]
        rd.shuffle(slots)

        for course in courses :
            for _ in range(course.hours_for_week) :
                if slots :
                    day, hour, classroom_index = slots.pop()
                    classroom = self.timetable[day][classroom_index]
                    classroom.hours[hour] = course
                else :
                    raise ValueError("Not enough slots available to schedule all courses")

    def __str__(self):
        result = []
        for day_index, day in enumerate(self.timetable) :
            day_result = [f"Day {day_index + 1}"]
            for classroom in day :
                day_result.append(str(classroom))
            result.append(day_result)
        return tabulate(result, tablefmt="plain")

if __name__ == "__main__":
    c1 = Course("ETC", "di nucci", 100, 8)
    c2 = Course("Math", "smith", 50,8)
    c3 = Course("Physics", "johnson", 75,8)
    d = Classroom("p1", 200)
    e = Classroom("p2", 100)
    time_table = Timetable([d,e])
    time_table.first_initialization([c1,c2,c3])
    print(time_table)