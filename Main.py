from Env import Timetable, Course, Classroom, Professor, Subjects
import GA

professors = [
    Professor("di nucci"),
    Professor("smith"),
    Professor("johnson"),
    Professor("lee"),
    Professor("kim"),
]

# Define courses and classrooms
courses = [
Course("ETC", professors[0], 200, 8, Subjects.COMPUTER_SCIENCE),
Course("Math", professors[1], 190, 7, Subjects.MATH, 3),
Course("Physics", professors[2], 75, 8, Subjects.PHYSICS),
Course("Programming", professors[3], 75, 9, Subjects.COMPUTER_SCIENCE, 3),
Course("Chemistry", professors[4], 100, 6, Subjects.CHEMISTRY),
Course("Biology", professors[0], 120, 6, Subjects.BIOLOGY),
Course("History", professors[1], 80, 6, Subjects.HISTORY),
Course("Geography", professors[2], 90, 4, Subjects.GEOGRAPHY),
Course("Art", professors[3], 60, 4, Subjects.ART),
Course("Music", professors[4], 50, 2, Subjects.MUSIC),
Course("Philosophy", professors[0], 60, 4, Subjects.PHILOSOPHY),
Course("Economics", professors[1], 80, 6, Subjects.ECONOMICS),
Course("Literature", professors[2], 70, 6, Subjects.LITERATURE),
Course("Sociology", professors[3], 85, 6, Subjects.SOCIOLOGY),
Course("Psychology", professors[4], 90, 8, Subjects.PSYCHOLOGY),
Course("Anthropology", professors[0], 65, 4, Subjects.ANTHROPOLOGY),
Course("Political Science", professors[1], 75, 7, Subjects.POLITICAL_SCIENCE, 3),
Course("Linguistics", professors[2], 55, 4, Subjects.LINGUISTICS),
Course("Astronomy", professors[3], 85, 6, Subjects.ASTRONOMY),
Course("Statistics", professors[4], 95, 9, Subjects.STATISTICS, 3),
Course("Programming 1", professors[0], 100, 9, Subjects.COMPUTER_SCIENCE, 3),
]

classrooms = [
    Classroom("p1", 200),
    Classroom("p2", 75),
    Classroom("p3", 100),
    Classroom("p4", 150),
    Classroom("p5", 90),
    Classroom("labCS", 200, True, Subjects.COMPUTER_SCIENCE),
    Classroom("labS", 95, True, Subjects.STATISTICS),
    Classroom("labPS", 90, True, Subjects.POLITICAL_SCIENCE),
    Classroom("labM", 200, True, Subjects.MATH),
]


def testing():
    agent1 = Timetable(classrooms, courses)
    timetable_data1 = [
        [[1, 1, 3, False],[1, 1, 4, False]],
        [[3, 1, 5, False],[3, 1, 6, False]]
]


    agent1.set_timetable(timetable_data1)
    GA.fitness(agent1)
    print(agent1.display_as_table())

# if __name__ == "__main__":
#     testing()

if __name__ == "__main__":
    import time

    agents = [Timetable(classrooms, courses) for _ in range(50)]

    start_time = time.time()
    result, fitness = GA.run(agents, generations=5000, mutation_rate=0.9, k=20, m=20)
    end_time = time.time()

    print(result.display_as_table())
    GA.fitness(result)
    print(f"Execution time: {end_time - start_time} seconds")